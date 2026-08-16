# Data dictionary and timing treatment

The table below summarizes the 30 source fields and how they should be treated in an ex-ante renewal-pricing study.

| Field | Meaning | Ex-ante treatment |
|---|---|---|
| `ID` | Internal annual-contract identifier; policyholders may have repeated annual records | Grouping and audit only; not a predictor |
| `Date_start_contract` | Contract start date | Derive policy tenure at renewal |
| `Date_last_renewal` | Current renewal reference date | Time index and chronological split |
| `Date_next_renewal` | Next renewal date | Exclude from predictors |
| `Date_birth` | Insured's birth date | Derive age at renewal; do not expose raw date |
| `Date_driving_licence` | Driver's licence issue date | Derive licence tenure; do not expose raw date |
| `Distribution_channel` | Agent or broker channel | Candidate pricing-time feature after code cleaning |
| `Seniority` | Relationship tenure with insurer | Ambiguous point-in-time field; reconstruct or exclude in strict analysis |
| `Policies_in_force` | Policies held in reference period | Candidate pricing-time feature |
| `Max_policies` | Historical maximum policies in force | Full-history ambiguity; exclude or reconstruct in strict analysis |
| `Max_products` | Historical maximum products held | Full-history ambiguity; exclude or reconstruct in strict analysis |
| `Lapse` | Current-year cancellation/nonpayment outcome | Exclude; post-pricing outcome |
| `Date_lapse` | Contract termination date | Exclude; post-pricing outcome |
| `Payment` | Annual or half-yearly payment method | Candidate pricing-time feature |
| `Premium` | Net premium for current annual policy period | Prediction target |
| `Cost_claims_year` | Current-year claim cost | Exclude; post-pricing outcome |
| `N_claims_year` | Current-year claim count | Exclude; post-pricing outcome |
| `N_claims_history` | Full-history claim count | Ambiguous timing; use only if reconstructed to the pricing date |
| `R_Claims_history` | Claim-frequency history ratio | Ambiguous timing; use only if reconstructed to the pricing date |
| `Type_risk` | Motorbike, van, passenger car, or agricultural vehicle | Candidate pricing-time feature |
| `Area` | Rural/urban indicator | Candidate pricing-time feature; geography is coarse |
| `Second_driver` | Multiple regular-driver indicator | Candidate pricing-time feature |
| `Year_matriculation` | Vehicle registration year | Derive vehicle age at renewal |
| `Power` | Vehicle horsepower | Candidate feature after invalid-zero treatment |
| `Cylinder_capacity` | Engine displacement | Candidate feature |
| `Value_vehicle` | Market value as of 2019-12-31 | Not historical point-in-time for 2015-2018 rows; exclude or replace in strict analysis |
| `N_doors` | Vehicle door count | Candidate feature; preserve zero as a flagged special-data pattern |
| `Type_fuel` | Petrol or diesel | Candidate feature after normalization |
| `Length` | Vehicle length in meters | Candidate feature with missingness flag |
| `Weight` | Vehicle weight in kilograms | Candidate feature |

## Verified data-quality observations

- 105,555 rows and 53,502 unique policy IDs.
- 10,329 missing `Length` values and 1,764 missing `Type_fuel` values.
- No missing target premiums; observed premium ranged from 40.14 to 2,993.34.
- Renewal dates ran from 2015-11-02 through 2018-11-30.
- 31 negative driving-experience values and 68 negative contract-age values were identified during the audit.
- Current lapse indicators and lapse dates disagreed in 18,351 rows.
- Several full-history variables appeared nearly constant across a policyholder's annual records, suggesting possible lifecycle backfilling.

## Two analysis specifications

### Reported baseline

The completed baseline excludes obvious post-renewal outcomes and uses 41 original and engineered features. Its out-of-time metrics are reported in the README and research report.

### Strict point-in-time extension

The planned extension will remove or reconstruct fields whose historical availability cannot be verified. It will also replace one-day inner validation folds with multi-date rolling windows and report both policy-row and policy-group robustness checks.
