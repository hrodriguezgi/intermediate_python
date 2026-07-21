import csv
import json
from pathlib import Path


def export_catalog(csv_path: Path, json_path: Path) -> dict:
    """
    Lee CSV de productos y genera JSON con resumen.

    Args:
        csv_path: Ruta al archivo CSV de productos
        json_path: Ruta donde escribir el JSON de salida

    Returns:
        Dict con: {"total_items": int, "inventory_units": int, "items": list}

    Hints:
        - Usa csv.DictReader para leer el CSV
        - Calcula total_items (cantidad de filas)
        - Calcula inventory_units (suma de la columna "stock")
        - Usa json.dumps() para convertir a JSON
    """
    # TODO: Implementa la función
    pass


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2] / "data"
    print(export_catalog(base / "products.csv", base / "catalog_export.json"))
