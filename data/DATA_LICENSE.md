# Dataset attribution and license

## Source

Lledó, Josep, and Pavía, Jose M. (2023). *Dataset of an actual motor vehicle insurance portfolio* (V1). Ann Arbor, MI: Inter-university Consortium for Political and Social Research [distributor]. https://doi.org/10.3886/E193182V1

- openICPSR project: https://www.openicpsr.org/openicpsr/project/193182/version/V1/view
- Principal investigators: Josep Lledó and Jose M. Pavía, University of Valencia
- Geographic coverage: Spain
- Time period: 2015-11-01 to 2018-12-01
- Source type: administrative records of an insurance company
- Dataset dimensions: 105,555 policy transactions by 30 variables

## License

The dataset is distributed under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/). The original authors and distributor retain attribution. The analytical code and documentation in this repository are separate from the dataset license.

## Repository copies

The original CSV has SHA-256 `51e492bacd76550c6b29c07af2ce4714c10685542b9988c22920d1bfb3ddbcc6`. To keep repository operations lightweight, it is split losslessly by row into five gzip-compressed CSV parts under `data/raw/`; every part repeats the original header and the notebook concatenates the parts automatically. No record-level values are modified.

The variable-description workbook is included as `data/raw/descriptive_of_variables.xlsx` and has SHA-256 `5caef82ce06efbe336aac72d37336dae5d17daaf478f1e742b3ba7a316babe6d`.

The split procedure is documented in `scripts/split_public_dataset.py`; the individual part hashes are reported in `data/raw/SHA256SUMS`.

## Responsible-use note

The source contains exact dates and other policy-level administrative variables. Public availability does not justify attempts to re-identify policyholders or link these records to external personal information. Follow the openICPSR terms and the CC BY 4.0 attribution requirement when reusing the data.
