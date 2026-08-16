"""Split the public source CSV into lossless, GitHub-friendly gzip parts."""

from __future__ import annotations

import gzip
import sys
from pathlib import Path


ROWS_PER_PART = 22_000


def split_csv(source: Path, destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    target = None

    try:
        with source.open("rb") as input_file:
            header = input_file.readline()
            for row_number, row in enumerate(input_file):
                if row_number % ROWS_PER_PART == 0:
                    if target is not None:
                        target.close()
                    part_number = row_number // ROWS_PER_PART + 1
                    output = destination / f"motor_vehicle_insurance_part_{part_number:02d}.csv.gz"
                    outputs.append(output)
                    target = gzip.GzipFile(output, mode="wb", mtime=0)
                    target.write(header)
                target.write(row)
    finally:
        if target is not None:
            target.close()

    return outputs


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: split_public_dataset.py SOURCE_CSV DESTINATION_DIRECTORY")
    for path in split_csv(Path(sys.argv[1]), Path(sys.argv[2])):
        print(path)
