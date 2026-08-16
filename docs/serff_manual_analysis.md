# SERFF rating-manual analysis

## Pilot document set

The current sample covers Progressive Select Insurance Company's Maryland Private Passenger Automobile Program materials dated October 2024:

- Rate Order of Calculation (clean and marked-up versions)
- Factor Pages (clean and marked-up versions)
- Rules manual (clean and marked-up versions)

The manuals were reviewed through the public SERFF filing-access context. They are not redistributed here; this repository contains analytical summaries only.

## Observed calculation architecture

The rate order is structurally different from a single unconstrained regression model.

### Stage 1: household/driver aggregation

The manual first constructs developed driver factors and combines them into a Household Risk Factor. When drivers outnumber vehicles, the rate order ranks drivers and averages the highest-ranked drivers up to the vehicle count.

### Stage 2: vehicle and coverage calculation

The household factor then enters a vehicle-level calculation that applies different components by coverage. The pilot manual includes the following broad categories.

| Factor family | Examples in pilot manual | Spanish-data correspondence |
|---|---|---|
| Driver and household | driver age, years licensed, driving record, household member/structure | age at renewal, licence tenure, second-driver indicator; household detail incomplete |
| Vehicle | symbol, attributes, age, ownership length, vehicle history, luxury/excess vehicle | age, value, power, engine size, doors, fuel, length, weight; symbols/history unavailable |
| Geography and use | garaging location, annual miles, business/rideshare use | only coarse urban/rural area; mileage/use largely unavailable |
| Coverage | base rate, limits, deductibles, full coverage, coverage-selection factors | coverage limits/deductibles absent in Spanish data |
| Insurance history | prior insurance, continuous insurance, tenure, accident/claim-free status | insurer tenure partly available; point-in-time history needs reconstruction |
| Transaction and payment | policy term, advance quote, online quote, paid-in-full, EFT, paperless, e-signature | payment and distribution channel available; quote timing/digital behavior absent |
| Tier and third-party data | tier, risk group, public/proprietary sourced data | not directly observed |
| Expenses and adjustments | expense loads, acquisition expense, rate stability, discounts/surcharges | observed premium is net; components not separately observed |

## Research implications

1. **Coverage normalization is essential.** Cross-carrier price comparison is not meaningful unless limits, deductibles, endorsements, and included coverages are standardized.
2. **Order matters.** A factor taxonomy alone is insufficient; the engine must preserve the rating sequence and factor applicability by coverage.
3. **Household-to-vehicle assignment matters.** A flat row-level model may miss explicit driver ranking and vehicle assignment rules.
4. **Observed premium is an incomplete label.** It aggregates risk, expenses, discounts, fees, and commercial adjustments.
5. **Versioning is mandatory.** A rating engine should identify carrier, state, program, effective date, filing version, and coverage.

## Proposed machine-readable schema

Each manual component will be represented by:

- carrier and underwriting company;
- state, program, and effective date;
- filing/document reference and page/table locator;
- calculation stage and sequence;
- rating level: household, driver, vehicle, policy, or coverage;
- factor name, input fields, table keys, and output scale;
- coverage applicability;
- eligibility conditions, caps, floors, and interactions;
- source status and review notes.

## Validation target

For a carrier-state-version combination with adequate inputs, the reconstructed engine should reproduce an authorized quote to rounding tolerance. When exact parity is impossible because a proprietary variable is unavailable, the engine should identify the unresolved component rather than silently absorbing it into an opaque residual.

## Public access references

- [SERFF Filing Access](https://www.serff.com/serff_filing_access.htm)
- [SERFF Filing Access - Maryland](https://filingaccess.serff.com/sfa/home/MD)
