"""Reusable utilities for the ex-ante motor-insurance pricing study.

The module separates deterministic feature construction from preprocessing and
model fitting. It does not download data or expose policy-level records.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATE_COLUMNS = [
    "Date_start_contract",
    "Date_last_renewal",
    "Date_next_renewal",
    "Date_lapse",
    "Date_birth",
    "Date_driving_licence",
]

CATEGORICAL_FEATURES = [
    "Distribution_channel",
    "Type_risk",
    "Type_fuel",
]

BINARY_FEATURES = [
    "Payment",
    "Area",
    "Second_driver",
    "flag_n_doors_zero",
    "flag_power_missing",
    "flag_type_fuel_missing",
    "flag_length_missing",
    "flag_negative_licence_tenure",
    "flag_licence_tenure_missing",
    "flag_young_driver",
    "flag_senior_driver",
    "flag_newly_licensed",
]

NUMERIC_FEATURES = [
    "Seniority",
    "Policies_in_force",
    "Max_policies",
    "Max_products",
    "Year_matriculation",
    "Power",
    "Cylinder_capacity",
    "Value_vehicle",
    "N_doors",
    "Length",
    "Weight",
    "age_at_renewal",
    "licence_tenure",
    "age_when_licensed",
    "vehicle_age",
    "policy_tenure",
    "renewal_year",
    "renewal_month",
    "renewal_quarter",
    "vehicle_value_log",
    "power_weight_ratio",
    "engine_cc_per_power",
    "value_per_vehicle_year",
    "weight_log",
    "length_log",
    "policy_headroom",
]

REPORTED_BASELINE_FEATURES = CATEGORICAL_FEATURES + BINARY_FEATURES + NUMERIC_FEATURES

POINT_IN_TIME_AMBIGUOUS = {
    "Seniority",
    "Max_policies",
    "Max_products",
    "Value_vehicle",
    "vehicle_value_log",
    "value_per_vehicle_year",
    "policy_headroom",
}

STRICT_POINT_IN_TIME_FEATURES = [
    feature
    for feature in REPORTED_BASELINE_FEATURES
    if feature not in POINT_IN_TIME_AMBIGUOUS
]

POST_PRICING_FIELDS = {
    "Lapse",
    "Date_lapse",
    "Cost_claims_year",
    "N_claims_year",
    "N_claims_history",
    "R_Claims_history",
}


@dataclass(frozen=True)
class DateBlockSplit:
    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def load_policy_data(path: str | Path) -> pd.DataFrame:
    """Load a locally authorized CSV and normalize accidental single-column reads."""

    path = Path(path)
    frame = pd.read_csv(path, low_memory=False)
    if frame.shape[1] == 1 and ";" in frame.columns[0]:
        frame = pd.read_csv(path, sep=";", low_memory=False)
    return frame


def _safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    return numerator / denominator.replace(0, np.nan)


def _safe_log(series: pd.Series, *, plus_one: bool = False) -> pd.Series:
    clean = series.where(series > 0)
    return np.log1p(clean) if plus_one else np.log(clean)


def build_pricing_features(raw: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic driver, vehicle, contract, and data-quality features."""

    frame = raw.copy()
    for column in DATE_COLUMNS:
        if column in frame:
            frame[column] = pd.to_datetime(frame[column], dayfirst=True, errors="coerce")

    distribution = frame["Distribution_channel"].astype("string").str.strip()
    distribution = distribution.replace(
        {
            "0.0": "0",
            "00": "0",
            "00/01/1900": "0",
            "1.0": "1",
            "01": "1",
        }
    )
    frame["Distribution_channel"] = distribution.where(distribution.isin(["0", "1"]))

    fuel = frame["Type_fuel"].astype("string").str.strip().str.upper()
    frame["Type_fuel"] = fuel.where(fuel.isin(["D", "P"]))

    frame["flag_n_doors_zero"] = frame["N_doors"].eq(0).astype("int8")
    frame["flag_power_missing"] = (
        frame["Power"].isna() | frame["Power"].eq(0)
    ).astype("int8")
    frame["flag_type_fuel_missing"] = frame["Type_fuel"].isna().astype("int8")
    frame["flag_length_missing"] = frame["Length"].isna().astype("int8")

    frame.loc[frame["Power"].eq(0), "Power"] = np.nan
    frame.loc[
        frame["Max_policies"].lt(frame["Policies_in_force"]), "Max_policies"
    ] = np.nan

    frame["age_at_renewal"] = (
        frame["Date_last_renewal"] - frame["Date_birth"]
    ).dt.days / 365.25
    frame["licence_tenure"] = (
        frame["Date_last_renewal"] - frame["Date_driving_licence"]
    ).dt.days / 365.25
    frame["age_when_licensed"] = (
        frame["Date_driving_licence"] - frame["Date_birth"]
    ).dt.days / 365.25
    frame["vehicle_age"] = (
        frame["Date_last_renewal"].dt.year - frame["Year_matriculation"]
    )
    frame["policy_tenure"] = (
        frame["Date_last_renewal"] - frame["Date_start_contract"]
    ).dt.days / 365.25

    frame["flag_negative_licence_tenure"] = frame["licence_tenure"].lt(0).astype("int8")
    frame.loc[frame["licence_tenure"].lt(0), "licence_tenure"] = np.nan
    frame.loc[frame["policy_tenure"].lt(0), "policy_tenure"] = np.nan
    frame.loc[frame["vehicle_age"].lt(0), "vehicle_age"] = np.nan

    frame["flag_licence_tenure_missing"] = frame["licence_tenure"].isna().astype("int8")
    frame["flag_young_driver"] = frame["age_at_renewal"].lt(25).astype("int8")
    frame["flag_senior_driver"] = frame["age_at_renewal"].ge(70).astype("int8")
    frame["flag_newly_licensed"] = (
        frame["licence_tenure"].notna() & frame["licence_tenure"].lt(2)
    ).astype("int8")

    frame["renewal_year"] = frame["Date_last_renewal"].dt.year
    frame["renewal_month"] = frame["Date_last_renewal"].dt.month
    frame["renewal_quarter"] = frame["Date_last_renewal"].dt.quarter

    frame["vehicle_value_log"] = _safe_log(frame["Value_vehicle"])
    frame["power_weight_ratio"] = _safe_divide(frame["Power"], frame["Weight"])
    frame["engine_cc_per_power"] = _safe_divide(
        frame["Cylinder_capacity"], frame["Power"]
    )
    frame["value_per_vehicle_year"] = _safe_divide(
        frame["Value_vehicle"], frame["vehicle_age"] + 1
    )
    frame["weight_log"] = _safe_log(frame["Weight"])
    frame["length_log"] = _safe_log(frame["Length"], plus_one=True)
    frame["policy_headroom"] = frame["Max_policies"] - frame["Policies_in_force"]

    return frame


def select_feature_set(frame: pd.DataFrame, specification: str = "reported") -> pd.DataFrame:
    """Return the completed-project or strict point-in-time feature matrix."""

    if specification == "reported":
        features = REPORTED_BASELINE_FEATURES
    elif specification == "strict":
        features = STRICT_POINT_IN_TIME_FEATURES
    else:
        raise ValueError("specification must be 'reported' or 'strict'")

    missing = sorted(set(features) - set(frame.columns))
    if missing:
        raise KeyError(f"Missing required feature columns: {missing}")
    return frame[features].copy()


def chronological_date_block_split(
    frame: pd.DataFrame,
    *,
    time_col: str = "Date_last_renewal",
    train_size: float = 0.60,
    validation_size: float = 0.20,
) -> DateBlockSplit:
    """Split complete date blocks so a renewal date cannot cross partitions."""

    if train_size <= 0 or validation_size <= 0 or train_size + validation_size >= 1:
        raise ValueError("train and validation sizes must be positive and sum to less than 1")

    ordered = frame.sort_values([time_col, "ID"]).reset_index(drop=True)
    dates = np.array(sorted(ordered[time_col].dropna().unique()))
    train_end = int(np.floor(len(dates) * train_size))
    validation_end = int(np.floor(len(dates) * (train_size + validation_size)))

    train_dates = dates[:train_end]
    validation_dates = dates[train_end:validation_end]
    test_dates = dates[validation_end:]

    return DateBlockSplit(
        train=ordered.loc[ordered[time_col].isin(train_dates)].copy(),
        validation=ordered.loc[ordered[time_col].isin(validation_dates)].copy(),
        test=ordered.loc[ordered[time_col].isin(test_dates)].copy(),
    )


def make_random_forest_pipeline(
    *,
    specification: str = "reported",
    n_estimators: int = 500,
    random_state: int = 42,
) -> Pipeline:
    """Build a transparent preprocessing pipeline and Random Forest baseline."""

    if specification == "reported":
        selected = REPORTED_BASELINE_FEATURES
    elif specification == "strict":
        selected = STRICT_POINT_IN_TIME_FEATURES
    else:
        raise ValueError("specification must be 'reported' or 'strict'")
    categorical = [c for c in CATEGORICAL_FEATURES if c in selected]
    binary = [c for c in BINARY_FEATURES if c in selected]
    numeric = [c for c in NUMERIC_FEATURES if c in selected]

    preprocessor = ColumnTransformer(
        [
            ("numeric", SimpleImputer(strategy="median"), numeric),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
            ("binary", SimpleImputer(strategy="most_frequent"), binary),
        ],
        remainder="drop",
    )

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    return Pipeline([("preprocess", preprocessor), ("model", model)])


def regression_metrics(actual: Iterable[float], predicted: Iterable[float]) -> dict[str, float]:
    """Return raw-premium MAE, RMSE, and R-squared."""

    actual_array = np.asarray(actual)
    predicted_array = np.asarray(predicted)
    return {
        "MAE": float(mean_absolute_error(actual_array, predicted_array)),
        "RMSE": float(np.sqrt(mean_squared_error(actual_array, predicted_array))),
        "R2": float(r2_score(actual_array, predicted_array)),
    }
