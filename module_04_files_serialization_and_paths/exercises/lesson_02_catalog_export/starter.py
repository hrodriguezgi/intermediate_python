import csv
import json
from pathlib import Path


def export_catalog(csv_path: Path, json_path: Path) -> dict:
    with csv_path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    payload = {
        "total_items": len(rows),
        "inventory_units": sum(int(row["stock"]) for row in rows),
        "items": rows,
    }
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return payload


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2] / "data"
    print(export_catalog(base / "products.csv", base / "catalog_export.json"))
