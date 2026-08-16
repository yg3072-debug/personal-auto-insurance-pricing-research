# SERFF rating-manual analysis

## Corrected scope

The manual work in this project concerns Maryland filings from Allstate entities. The core research object is the rating logic disclosed in Private Passenger Auto rate and rule manuals. A separate motorcycle filing memorandum is used only as background for actuarial rate-level indication methods; it is not treated as a personal-auto tariff.

The source PDFs are not redistributed in this repository. This document records the reviewed inventory, analytical protocol, source-page conventions, and limitations.

## Reviewed document inventory

| Underwriting company | Filing/material | Product and role | Date evidence in supplied file |
|---|---|---|---|
| Allstate Indemnity Company | R59063 A2 Rates Manual, with accompanying rule references | Maryland Voluntary Private Passenger Auto; 51-step pilot calculation | RP-2A effective 2026-09-04 |
| Allstate North American Insurance Company | R57301 A1 Rates Manual and A2 Rules Manual | Maryland Private Passenger Auto; earlier plan version | RP-1A dated 2024-04-16; rules index dated 2025-03-21 |
| Allstate North American Insurance Company | R58046 A3 Rates and Rules Manuals | Maryland Private Passenger Auto; amended plan | RP-2A and manual overrides dated 2025-09-06 |
| Allstate North American Insurance Company | R59113 Complete Manual | Consolidated Maryland Private Passenger Auto rate and rule material | contains 2025-09-06 plan pages and overrides |
| Allstate North American Insurance Company | R60248 Complete Rates Manual | Maryland Private Passenger Auto rate update | RP-3A dated 2026-05-02 |
| Allstate Property and Casualty Insurance Company | R59171 filing memorandum | Maryland Motorcycle; actuarial-indication context only | filing exhibits reference 2024-2025 experience and standards |

Filing identifiers and page dates are both retained because a compiled manual can contain legacy pages, current pages, and manual overrides with different effective dates. The latest date printed in a PDF is not automatically assigned to every page.

## Two observed rating architectures

### Allstate Indemnity R59063: 51-step sequence

The RP-2A page provides the calculation backbone. Its ordered steps move through:

1. **Coverage starting values:** territorial base rates, rate adjustment, increased limits, and UM/EUIM limit treatment.
2. **Policy and household classification:** supplementary multiplicative patterns, insurance-score and rating tiers, package selection, policy class, household composition, discounts, prior insurance, accident and violation surcharges, and mandatory good-driver treatment.
3. **Vehicle classification:** model year, deductible/price group, experience-group rating, Drivewise, mileage, usage, safety equipment, new-car treatment, replacement protection, gap, ride-for-hire, and table-assignment group factors.
4. **Expense and aggregation:** fixed expense, vehicle subtotals, excess medical, miscellaneous coverages, and total semiannual policy premium.

The important analytical property is not merely the list of factors. RP-2A specifies sequence, coverage columns, multiplication versus addition, intermediate rounding, and subtotal logic.

### Allstate North American: roughly 69-71 calculation lines

The Allstate North American manuals use a different plan architecture. The main vehicle calculation includes base rate, rate adjustment, territorial relativity, limits, PIP option, household composition, insurance-score and rating tiers, accident and violation programs, payment and channel factors, underwriting tier, bad-debt risk, discounts, telematics participation, mobile and vehicle driving factors, vehicle characteristics, mileage, vehicle history and technology, variable interactions, rate mitigation, rate-level management, and fixed expense. Separate blocks calculate other PIP coverages, UMPD/EUIMPD, and miscellaneous coverages before the policy total.

This provides a useful within-carrier-family comparison: two underwriting companies can disclose materially different factor systems and calculation orders even within the same state and broad product category.

## Six-stage analysis protocol

### 1. Inventory and effective-date control

For every source file and page, record:

- underwriting company, state, product, filing number, amendment, and document type;
- page identifier, printed effective date, source filename, and extraction status;
- whether the page is current, superseded, overridden, or uncertain.

This prevents a compiled manual from being treated as if every page belonged to one effective date.

### 2. Calculation-graph reconstruction

Use the premium-calculation page as the spine of an ordered directed graph. Each node records:

- sequence number and factor name;
- operation: lookup/base, multiply, add, subtotal, or final sum;
- rating level: household, policy, driver, vehicle, or coverage;
- coverage applicability and fallback rules;
- rounding point and upstream dependencies.

Order must be preserved because additive amounts, per-coverage factors, subtotals, and rounding generally do not commute.

### 3. Rule-to-table linkage

For each graph node, follow the cited rate page and rule. Separate four concepts that are often mixed together:

1. **Eligibility:** whether the factor applies.
2. **Input construction:** how a tier, value, score group, or household count is created.
3. **Lookup:** which row and column produce the factor or addend.
4. **Application:** which coverage receives the result and at what point in the sequence.

Every extracted value retains its rate-page, rule, table, row-key, and coverage-column provenance.

### 4. Machine-readable extraction and QA

Normalize each factor into a versioned schema containing input keys, categorical ranges, numeric bounds, output factors/addends, coverage mapping, exceptions, and source location. Automated text or table extraction is treated as a draft. Representative rows, boundary values, merged headers, footnotes, and cross-page tables are checked manually.

The companion [`manual_factor_schema.yaml`](manual_factor_schema.yaml) shows the proposed structure without reproducing full proprietary or copyrighted manuals.

### 5. Version comparison

Compare manuals at the semantic-node level rather than by raw PDF text. The version-difference report classifies:

- added or removed factors;
- renamed factors with equivalent logic;
- changed table values or category boundaries;
- changed coverage applicability or calculation order;
- new overrides, caps, floors, mitigation, or transition rules.

This distinguishes a true rating-plan change from pagination, formatting, or filing-package noise.

### 6. Scenario execution and validation

Create standardized applicant-policy-vehicle profiles and execute them through the graph. Validation proceeds in layers:

1. hand-check selected lookups and intermediate steps;
2. verify subtotals, rounding, and final aggregation;
3. compare with authorized quote examples when available;
4. report unexplained components by source and coverage.

If a proprietary score, vehicle group, interaction, or underwriting input cannot be reproduced, it remains an explicit unresolved node rather than being hidden in a residual.

## Crosswalk to the Spanish policy data

| Manual requirement | Spanish data status | Research treatment |
|---|---|---|
| Driver age and licence tenure | available from dates | reconstruct at each renewal date |
| Household/second-driver structure | partial | retain second-driver indicator; identify missing operator detail |
| Distribution channel and payment | available | align definitions before comparison |
| Territory | coarse urban/rural only | cannot reproduce Maryland territorial tables |
| Vehicle age, value, power, size, and fuel | partly available | audit timing and code quality; map only defensible fields |
| Prior insurance and claims history | partial and timing-ambiguous | reconstruct or exclude from strict specification |
| Coverage limits and deductibles | unavailable | required in future quote-data schema |
| Insurance score, rating/underwriting tier, violations | unavailable | treat as missing or proprietary inputs |
| Mileage, telematics, vehicle-driving score | unavailable | future consented collection only |
| Vehicle history/technology groups and interactions | unavailable | unresolved manual nodes unless an authorized source is found |

The crosswalk prevents the empirical model from being described as a tariff reconstruction. It also turns missing manual inputs into a concrete data-collection plan for the proposed comparison platform.

## Research implications

1. **Premium prediction is not tariff reconstruction.** The Spanish target combines risk classification, coverage, expenses, discounts, and commercial rules.
2. **Coverage normalization is essential.** Prices cannot be compared without aligning limits, deductibles, endorsements, and included coverages.
3. **Versioning is mandatory.** Carrier, underwriting company, state, program, filing, page date, and rule version must travel with every factor.
4. **Source traceability is part of validation.** A factor without a page/table/rule reference is not considered production-ready.
5. **Scope must remain explicit.** The motorcycle filing memo informs actuarial context but is not evidence for a personal-auto premium step.

## Public access references

- [SERFF Filing Access](https://www.serff.com/serff_filing_access.htm)
- [SERFF Filing Access - Maryland](https://filingaccess.serff.com/sfa/home/MD)
