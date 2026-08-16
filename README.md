# Ex-Ante Personal Auto Insurance Pricing

A leakage-aware study of renewal-premium prediction using 105,555 annual policy records from a Spanish motor insurer, extended with a structured review of public U.S. personal-auto rate manuals.

## Why this project matters

An insurance premium is not simply a claim-cost forecast. It reflects an insurer's rating plan: base rates, driver and household characteristics, vehicle attributes, coverage choices, territory, discounts, surcharges, expenses, and the order in which those components are applied. This project studies both sides of that problem:

1. **Empirical pricing model:** identify patterns in observed renewal premiums using information intended to be available at pricing time.
2. **Regulatory-manual analysis:** translate publicly filed rating rules into a transparent, auditable factor taxonomy and calculation sequence.

The long-term research goal is a consumer-facing comparison framework that can normalize an applicant's risk profile, compare quotes across carriers, and explain material price differences without representing a quote as a binding offer.

## Current empirical study

| Item | Verified value |
|---|---:|
| Annual policy observations | 105,555 |
| Unique policy IDs | 53,502 |
| Renewal-date range | 2015-11-02 to 2018-11-30 |
| Candidate modeling features | 41 |
| Final model | Random Forest on `log1p(Premium)` |
| Out-of-time test MAE | 55.08 |
| Out-of-time test RMSE | 91.05 |
| Out-of-time test R-squared | 0.573 |

The data were split by renewal-date blocks rather than randomly. The final test block contained 25,194 later policy observations and was used only after model selection.

### Main analytical findings

- Tree ensembles captured the premium structure better than linear and regularized baselines, consistent with nonlinearities and interactions in the observed tariff.
- Vehicle-value intensity, payment method, policy tenure, vehicle-record anomalies, driver experience, distribution channel, and multiple-driver status were among the strongest predictive signals.
- The model compressed the tails: high premiums tended to be underpredicted and low premiums tended to be overpredicted.
- Predictive importance is not causal risk importance. The target is the insurer's observed premium, so the model partly learns the incumbent rating plan and operational data patterns.

## SERFF manual extension

The current manual panel covers Maryland filings for **Allstate Indemnity Company** and **Allstate North American Insurance Company**, rather than Progressive:

- Allstate Indemnity filing **R59063**: a 51-step RP-2A premium calculation effective September 4, 2026.
- Allstate North American filings **R57301, R58046, R59113, and R60248**: rate and rule materials spanning 2024-2026, with a roughly 69-71-line architecture.

The analysis does more than list factors. It inventories effective pages and overrides, converts the premium-calculation order into a directed graph, links each node to its rule and lookup table, records coverage applicability and additive versus multiplicative treatment, compares versions, and validates standardized profiles by hand or against authorized quotes. Representative rating dimensions include territory and limits; household, insurance-score, rating, accident, and violation tiers; payment and channel; telematics and driving behavior; vehicle characteristics, mileage, history, and technology; interactions, mitigation, and fixed expense.

The repository does not redistribute insurer manuals. It records document inventory, source-page references, analytical workflow, and a machine-readable example with links to public SERFF access. See [`docs/serff_manual_analysis.md`](docs/serff_manual_analysis.md) and [`docs/manual_factor_schema.yaml`](docs/manual_factor_schema.yaml).

## Important methodological boundary

The completed baseline removed obvious post-renewal outcomes such as current-year claims and lapse outcomes. A later audit identified additional point-in-time ambiguity in several full-history fields and in a vehicle-value field defined as of 2019. The reported metrics above belong to the completed baseline; they should not be presented as results from the stricter feature specification until that robustness analysis is rerun.

This distinction is deliberate:

- **Reported baseline:** reproduces the completed project and resume metrics.
- **Strict point-in-time extension:** reconstructs historical values, removes or lags ambiguous fields, and uses wider rolling validation windows.

## Repository guide

```text
.
├── data/                  # Public source data, provenance, and license notes
├── docs/                  # Data dictionary, methods, SERFF analysis, roadmap
├── notebooks/             # Cleaned source notebook; outputs removed
├── reports/               # Completed research report
├── src/                   # Reusable feature and validation utilities
├── tests/                 # Synthetic-data unit tests
└── requirements.txt
```

## Reproduce the workflow

The original 105,555-row dataset is included as five lossless gzip-compressed row parts under `data/raw/`. It is publicly distributed by openICPSR and licensed under CC BY 4.0. The notebook discovers and concatenates the parts automatically.

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the notebook from top to bottom. Full tuning is computationally expensive; use fixed parameters for a portfolio review and reserve full chronological search for formal replication.
3. Run tests with `pytest -q`.

## Data provenance and attribution

The empirical analysis uses the public **Dataset of an actual motor vehicle insurance portfolio**, which contains 105,555 policy transactions from a Spanish insurer covering November 2015 through December 2018.

> Lledó, Josep, and Pavía, Jose M. (2023). *Dataset of an actual motor vehicle insurance portfolio* (V1). Inter-university Consortium for Political and Social Research. https://doi.org/10.3886/E193182V1

- [openICPSR project page](https://www.openicpsr.org/openicpsr/project/193182/version/V1/view)
- License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
- Local integrity record: [`data/DATA_LICENSE.md`](data/DATA_LICENSE.md)

## Research roadmap

The next phase will expand the project from premium prediction to transparent tariff reconstruction and quote comparison:

- reconstruct point-in-time features and evaluate grouped, rolling out-of-time splits;
- collect standardized, consented quote snapshots across carriers and time;
- encode additional SERFF manuals into a carrier-state-version factor schema;
- compare filed factor logic with empirical sensitivities and quote differences;
- quantify calibration, tail error, temporal stability, and subgroup performance;
- build a research prototype that links vehicle owners, a comparison platform, and insurer-facing rating logic.

See [`docs/research_roadmap.md`](docs/research_roadmap.md) for scope and evaluation criteria.

## Sources and use

- [Lledó and Pavía motor-insurance dataset, openICPSR](https://doi.org/10.3886/E193182V1)
- [SERFF Filing Access](https://www.serff.com/serff_filing_access.htm)
- [SERFF Filing Access - Maryland](https://filingaccess.serff.com/sfa/home/MD)

This repository is a research and portfolio project. It does not provide actuarial certification, legal advice, underwriting decisions, or binding insurance quotes.
