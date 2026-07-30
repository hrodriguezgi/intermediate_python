"""
Phase 1: Data Loading & Validation

Objetivos:
- Cargar CSV con manejo de errores
- Validar tipos de datos
- Manejar datos faltantes
- Información sobre el dataset
"""

from pathlib import Path
import csv
from typing import List, Dict, Any


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "products.csv"


# TODO: Implementar función para cargar CSV
def load_products_csv(filepath: Path) -> List[Dict[str, Any]]:
    """
    Cargar CSV de productos.

    Debe:
    1. Leer el archivo con encoding correcto (UTF-8)
    2. Convertir a lista de dicts
    3. Validar que cada row tenga los campos esperados
    4. Convertir tipos de datos (price -> float, stock -> int)

    Args:
        filepath: Ruta al archivo CSV

    Returns:
        Lista de productos validados

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si hay errores de formato
    """
    pass  # TODO


# TODO: Implementar validación de cada row
def validate_product(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validar y convertir tipos de un producto.

    Debe:
    1. Verificar que no falten campos obligatorios
    2. Convertir price a float
    3. Convertir stock a int
    4. Validar que price > 0
    5. Validar que stock >= 0

    Argumentos:
        row: Dict con datos del producto

    Returns:
        Row validado y convertido

    Raises:
        ValueError: Si validación falla
    """
    pass  # TODO


# TODO: Implementar función para obtener estadísticas
def print_data_summary(products: List[Dict[str, Any]]) -> None:
    """
    Imprimir información sobre los datos cargados.

    Debe mostrar:
    - Total de productos
    - Categorías disponibles
    - Rango de precios
    - Stock total
    - Productos con bajo stock (< 20)
    """
    pass  # TODO


if __name__ == "__main__":
    # Cargar datos
    print(f"Loading data from {CSV_PATH}...")

    try:
        products = load_products_csv(CSV_PATH)
        print(f"✓ Loaded {len(products)} products")

        # Mostrar resumen
        print_data_summary(products)

        # Mostrar algunos productos
        print("\nFirst 3 products:")
        for p in products[:3]:
            print(f"  {p}")

    except FileNotFoundError:
        print(f"✗ File not found: {CSV_PATH}")
    except Exception as e:
        print(f"✗ Error: {e}")
