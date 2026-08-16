"""Create a public, output-free copy of the completed analysis notebook."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(source: str, destination: str) -> None:
    source_path = Path(source)
    destination_path = Path(destination)
    notebook = json.loads(source_path.read_text(encoding="utf-8"))

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        cell["outputs"] = []
        cell["execution_count"] = None
        source_text = "".join(cell.get("source", []))
        source_text = source_text.replace(
            'pd.read_csv("D:/JNP/Motor vehicle insurance data.csv")',
            'from pathlib import Path\n\n'
            'pd.concat(\n'
            '    (pd.read_csv(path) for path in sorted(\n'
            '        Path("../data/raw").glob("motor_vehicle_insurance_part_*.csv.gz")\n'
            '    )),\n'
            '    ignore_index=True,\n'
            ')',
        )
        cell["source"] = source_text.splitlines(keepends=True)

    metadata = notebook.setdefault("metadata", {})
    metadata.pop("widgets", None)
    metadata["portfolio_note"] = (
        "Outputs removed to avoid publishing policy-level records. "
        "Aggregate results are documented in the report and README."
    )
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: prepare_portfolio_notebook.py SOURCE DESTINATION")
    main(sys.argv[1], sys.argv[2])
