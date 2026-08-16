import numpy as np
import pandas as pd

from src.insurance_pricing import (
    POST_PRICING_FIELDS,
    REPORTED_BASELINE_FEATURES,
    STRICT_POINT_IN_TIME_FEATURES,
    build_pricing_features,
    chronological_date_block_split,
    make_random_forest_pipeline,
    select_feature_set,
)


def synthetic_policies(rows: int = 48) -> pd.DataFrame:
    index = np.arange(rows)
    renewal = pd.Timestamp("2017-01-01") + pd.to_timedelta(index // 4, unit="D")
    return pd.DataFrame(
        {
            "ID": index + 1,
            "Date_start_contract": renewal - pd.to_timedelta(365 + index, unit="D"),
            "Date_last_renewal": renewal,
            "Date_next_renewal": renewal + pd.to_timedelta(365, unit="D"),
            "Date_birth": pd.Timestamp("1970-01-01") + pd.to_timedelta(index * 30, unit="D"),
            "Date_driving_licence": pd.Timestamp("1990-01-01") + pd.to_timedelta(index * 10, unit="D"),
            "Distribution_channel": np.where(index % 2, 1, 0),
            "Seniority": 1 + index % 8,
            "Policies_in_force": 1 + index % 2,
            "Max_policies": 2 + index % 3,
            "Max_products": 1 + index % 3,
            "Lapse": 0,
            "Date_lapse": pd.NaT,
            "Payment": index % 2,
            "Premium": 150 + index * 4.5,
            "Cost_claims_year": 0,
            "N_claims_year": 0,
            "N_claims_history": index % 3,
            "R_Claims_history": (index % 3) / 4,
            "Type_risk": 1 + index % 4,
            "Area": index % 2,
            "Second_driver": (index // 2) % 2,
            "Year_matriculation": 2002 + index % 12,
            "Power": 70 + index % 60,
            "Cylinder_capacity": 1200 + index * 10,
            "Value_vehicle": 7000 + index * 250,
            "N_doors": np.where(index % 10 == 0, 0, 4),
            "Type_fuel": np.where(index % 2, "D", "P"),
            "Length": 3.8 + (index % 8) / 10,
            "Weight": 1000 + index * 8,
        }
    )


def test_feature_construction_and_leakage_boundary():
    featured = build_pricing_features(synthetic_policies())
    baseline = select_feature_set(featured, "reported")
    strict = select_feature_set(featured, "strict")

    assert baseline.shape[1] == 41
    assert list(baseline.columns) == REPORTED_BASELINE_FEATURES
    assert list(strict.columns) == STRICT_POINT_IN_TIME_FEATURES
    assert POST_PRICING_FIELDS.isdisjoint(baseline.columns)
    assert baseline["flag_n_doors_zero"].sum() > 0


def test_date_blocks_do_not_overlap():
    featured = build_pricing_features(synthetic_policies())
    split = chronological_date_block_split(featured)

    train_dates = set(split.train["Date_last_renewal"])
    validation_dates = set(split.validation["Date_last_renewal"])
    test_dates = set(split.test["Date_last_renewal"])

    assert train_dates.isdisjoint(validation_dates)
    assert train_dates.isdisjoint(test_dates)
    assert validation_dates.isdisjoint(test_dates)
    assert max(train_dates) < min(validation_dates) < min(test_dates)


def test_pipeline_fits_synthetic_records():
    featured = build_pricing_features(synthetic_policies())
    features = select_feature_set(featured, "strict")
    model = make_random_forest_pipeline(specification="strict", n_estimators=10)

    model.fit(features, np.log1p(featured["Premium"]))
    predictions = np.expm1(model.predict(features.head(5)))

    assert predictions.shape == (5,)
    assert np.isfinite(predictions).all()
    assert (predictions > 0).all()
