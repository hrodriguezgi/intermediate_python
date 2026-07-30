import csv
import json
from pathlib import Path


def export_catalog(csv_path: Path, json_path: Path) -> str:
    """
    Lee CSV de productos y genera JSON con resumen.

    Args:
        csv_path: Ruta al archivo CSV de productos
        json_path: Ruta donde escribir el JSON de salida

    Returns:
        str (json) con: {"total_items": int, "inventory_units": int, "items": list}

    Hints:
        - Usa csv.DictReader para leer el CSV
        - Calcula total_items (cantidad de filas)
        - Calcula inventory_units (suma de la columna "stock")
        - Devolver la lista de objetos en items
        - Usa json.dump() para convertir a JSON
    """
    # TODO: Implementa la función
    salida = {"total_items": 0, "inventory_units": 0, "items": list()}

    with csv_path.open(encoding="utf-8") as origen:
        registros = list(csv.DictReader(origen))

    salida["total_items"] = len(registros)
    salida["inventory_units"] = sum(int(registro["stock"]) for registro in registros)
    salida["items"] = registros

    with json_path.open("w", encoding="utf-8") as archivo_salida:
        json.dump(salida, archivo_salida, indent=2)

    return "Guardado exitosamente"


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2] / "data"
    print(export_catalog(base / "products.csv", base / "catalog_export.json"))
