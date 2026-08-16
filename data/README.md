# Data source, access, and responsible use

The completed study used 105,555 annual policy observations from a Spanish motor insurer. The original public dataset and its variable-description workbook are included in `data/raw/` so the empirical workflow can be reproduced directly.

## Public source

Lledó, Josep, and Pavía, Jose M. (2023). *Dataset of an actual motor vehicle insurance portfolio* (V1). Inter-university Consortium for Political and Social Research. https://doi.org/10.3886/E193182V1

- Project page: https://www.openicpsr.org/openicpsr/project/193182/version/V1/view
- Geographic coverage: Spain
- Observation period: November 2015 to December 2018
- Unit of observation: policy transaction
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)

## Included files

```text
data/raw/motor_vehicle_insurance_part_01.csv.gz
data/raw/motor_vehicle_insurance_part_02.csv.gz
data/raw/motor_vehicle_insurance_part_03.csv.gz
data/raw/motor_vehicle_insurance_part_04.csv.gz
data/raw/motor_vehicle_insurance_part_05.csv.gz
data/raw/descriptive_of_variables.xlsx
```

Together, the five compressed CSV parts contain all 105,555 data rows and 30 columns. They are split losslessly by row and each part repeats the original header. The notebook loads and concatenates them automatically. See [`DATA_LICENSE.md`](DATA_LICENSE.md) for attribution, file hashes, and license details.

## Expected schema

The source contains 30 fields covering:

- policy ID and contract/renewal dates;
- driver birth and licence dates;
- distribution channel, payment, area, and policy structure;
- premium, claims, and lapse fields;
- vehicle type, age, value, power, engine capacity, doors, fuel, length, and weight.

See [`../docs/data_dictionary.md`](../docs/data_dictionary.md) for field definitions and timing treatment.

## Reproducibility boundary

The dataset is publicly licensed, but it contains exact dates and policy-level administrative fields. Users should not attempt to identify policyholders, link records to external personal information, or use the data to make decisions about identifiable individuals. The ID field is used for grouping and audit rather than as a model feature.

Tests in this repository continue to use synthetic records so that unit tests remain fast and do not depend on individual source observations.
