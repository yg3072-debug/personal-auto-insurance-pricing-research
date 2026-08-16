# Methodology

## Research question

Can renewal premiums be predicted and explained using only information defensibly available at the pricing date, and how closely do those empirical relationships correspond to the factor structure disclosed in insurer rate manuals?

## Completed workflow

1. **Data audit:** check categorical codes, date logic, missingness patterns, vehicle anomalies, and cross-field consistency.
2. **Timing screen:** exclude current-year claims, lapse outcomes, lapse dates, and ambiguous full-life claim summaries from the baseline predictor set.
3. **Feature engineering:** construct driver age, licence tenure, vehicle age, policy tenure, renewal calendar, value/intensity ratios, and anomaly indicators.
4. **Chronological split:** sort by renewal date and divide unique date blocks into train, validation, and final test periods.
5. **Model comparison:** compare OLS, Ridge, Lasso, Elastic Net, Random Forest, Extra Trees, Gradient Boosting, and HistGradientBoosting on raw and log-transformed targets.
6. **Selection and testing:** tune candidates on the training period, select using the validation period, refit on train plus validation, and evaluate once on the later test block.
7. **Interpretation:** use permutation importance, SHAP, residual summaries, and tail-case review.

## Verified split

| Split | Rows | Unique IDs | Renewal dates |
|---|---:|---:|---|
| Train | 58,775 | 38,715 | 2015-11-02 to 2017-09-06 |
| Validation | 21,586 | 21,586 | 2017-09-07 to 2018-04-19 |
| Test | 25,194 | 25,194 | 2018-04-20 to 2018-11-30 |

The same policy ID may appear in an earlier and a later outer split because the task predicts later renewals from earlier observations. This is a valid operational framing, but a grouped holdout is also useful as a robustness check for generalization to unseen policies.

## Completed-model result

The selected Random Forest was trained on `log1p(Premium)` and achieved MAE 55.08, RMSE 91.05, and R-squared 0.573 on the untouched later test block.

These metrics estimate fidelity to observed charged premium, not expected claim cost, rate adequacy, or causal risk. The model learns a mixture of risk classification, rating-plan structure, commercial decisions, and administrative data patterns.

## Limitations that define the next study

1. **Point-in-time ambiguity:** several relationship-history fields and the 2019 vehicle-value field may not be historically valid for earlier renewals.
2. **Narrow inner folds:** the initial tuning procedure used single-date validation folds with 66-86 observations. Wider rolling windows are needed for more stable parameter selection.
3. **Repeated policies:** chronological evaluation matches renewal deployment, but it does not separately measure performance on entirely unseen policyholders.
4. **Tail compression:** the model underpredicts high premiums and overpredicts low premiums.
5. **Premium is not loss cost:** without exposure, coverage, expense, and claim-severity/frequency data, the model cannot establish an actuarially indicated premium.
6. **Manual correspondence is incomplete:** current factor comparisons are structural, not yet a carrier-level tariff reconstruction with quote-parity testing.

## Planned robustness protocol

- Reconstruct each candidate feature as of the renewal date.
- Use rolling multi-month validation windows and a protected final time block.
- Compare policy-row and policy-group holdouts.
- Report MAE, RMSE, R-squared, calibration by premium decile, tail MAE, and temporal stability.
- Use bootstrapped confidence intervals for model differences.
- Evaluate subgroup error only where sample size and lawful use permit; treat fairness analysis as diagnostic, not as a legal conclusion.
