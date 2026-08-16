# Research roadmap

## Proposed next-phase question

How can policy data, standardized quote observations, and public insurer rate manuals be combined into a transparent ex-ante personal-auto pricing framework that predicts premiums, reconstructs material rating logic, and explains cross-carrier quote differences?

## Workstream 1: point-in-time empirical model

- rebuild driver, vehicle, policy, and claim-history features as of each renewal date;
- compare interpretable GLM/GAM baselines with Random Forest, gradient boosting, and CatBoost-style models;
- use rolling multi-date validation and an untouched later test period;
- quantify calibration, tail error, stability, uncertainty, and subgroup performance;
- distinguish premium imitation from expected-loss modeling.

## Workstream 2: manual-to-engine translation

- complete and validate the 51-step Allstate Indemnity R59063 calculation graph;
- encode selected Allstate North American R57301/R58046/R59113/R60248 factor tables, rules, coverage applicability, and calculation order;
- compare underwriting-company and effective-date versions before expanding to a cross-carrier panel;
- test scenario-based tariff reconstruction against hand calculations and authorized quote examples.

## Workstream 3: standardized quote panel

- define a consented, auditable data-collection protocol;
- hold driver, vehicle, geography, coverage, and quote timing constant when comparing carriers;
- record quote metadata, coverage definitions, and manual version;
- avoid collecting credentials, unnecessary personal identifiers, or data contrary to site terms.

## Workstream 4: research platform prototype

The prototype will demonstrate the data and explanation layer required to connect three groups:

- **Vehicle owners:** provide a normalized risk profile and coverage preferences; receive comparable, source-traceable explanations.
- **Comparison platform:** validates inputs, normalizes coverage, invokes carrier/version logic, and records consent and provenance.
- **Insurers or carrier modules:** provide filed/manual factor logic or quote outputs without exposing unsupported proprietary claims.

The semester deliverable is a research prototype, not a licensed marketplace or binding-quote system.

## Evaluation criteria

| Component | Primary criterion |
|---|---|
| Premium model | out-of-time MAE/RMSE, calibration, tail error, stability |
| Strict timing audit | no feature uses information unavailable at quote/renewal time |
| Manual parser/schema | factor coverage, source traceability, version completeness |
| Rating reconstruction | quote parity or clearly identified unresolved residuals |
| Cross-carrier comparison | coverage-normalized price differences and explanation consistency |
| Prototype | reproducible end-to-end flow with privacy and source controls |

## One-semester sequence

1. **Weeks 1-3:** point-in-time audit, literature review, data and manual schema.
2. **Weeks 4-6:** strict baseline and rolling validation.
3. **Weeks 7-10:** manual encoding and quote-panel pilot.
4. **Weeks 11-13:** rating comparison and prototype integration.
5. **Weeks 14-15:** robustness checks, documentation, and final report.
