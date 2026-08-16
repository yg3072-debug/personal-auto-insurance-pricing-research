# Data access and privacy

The completed study used 105,555 annual policy observations from a Spanish motor insurer. The raw file is not included in this public repository.

## Why the raw data are excluded

Although the dataset does not contain names, it includes exact dates of birth, driving-licence dates, renewal dates, policy IDs, vehicle characteristics, and insurance outcomes. These fields can function as quasi-identifiers when combined. A public redistribution license was also not established.

## Expected local path

Place an authorized local copy at:

```text
data/raw/motor_vehicle_insurance.csv
```

The `.gitignore` file prevents this directory from being committed.

## Expected schema

The source contains 30 fields covering:

- policy ID and contract/renewal dates;
- driver birth and licence dates;
- distribution channel, payment, area, and policy structure;
- premium, claims, and lapse fields;
- vehicle type, age, value, power, engine capacity, doors, fuel, length, and weight.

See [`../docs/data_dictionary.md`](../docs/data_dictionary.md) for field definitions and timing treatment.

## Reproducibility boundary

The report and repository document verified aggregate counts and model metrics. Reproducing those results requires the authorized source file. Tests in this repository use synthetic records only and do not recreate or approximate any individual policyholder.
