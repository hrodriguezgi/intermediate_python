"""
Phase 4: DuckDB Analytics

Objetivos:
- Queries analíticas rápidas
- GROUP BY, agregaciones
- Performance vs SQLite
"""

import duckdb
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path(__file__).resolve().parent
ANALYTICS_DB = BASE_DIR / "data" / "analytics.duckdb"
CSV_PATH = BASE_DIR / "data" / "products.csv"


class AnalyticsEngine:
    """Motor analítico basado en DuckDB."""

    def __init__(self, db_path: Path):
        self.conn = duckdb.connect(str(db_path))

    # TODO: Cargar CSV en tabla DuckDB
    def load_products_from_csv(self, csv_path: Path) -> None:
        """
        Cargar datos de CSV a tabla DuckDB.

        Debe:
        1. Leer CSV
        2. Crear tabla 'products'
        3. Insertar datos
        """
        pass

    # TODO: Top 10 productos por categoría
    def top_products_by_category(self, category: str, limit: int = 10) -> List[Tuple]:
        """
        Obtener productos más caros de una categoría.

        Args:
            category: Nombre de categoría
            limit: Cantidad de productos a retornar

        Returns:
            Lista de (name, price, stock)
        """
        pass

    # TODO: Estadísticas por categoría
    def category_statistics(self) -> List[Tuple]:
        """
        Obtener estadísticas de inventario por categoría.

        Debe retornar (category, product_count, total_value, avg_price).

        Returns:
            Lista de tuplas (category, count, total_value, avg_price)
        """
        pass

    # TODO: Productos con bajo stock
    def low_stock_alert(self, threshold: int = 20) -> List[Tuple]:
        """
        Productos con stock bajo.

        Args:
            threshold: Nivel de stock considerado bajo

        Returns:
            Lista de (name, category, stock)
        """
        pass

    # TODO: Total de inventario
    def total_inventory_value(self) -> float:
        """
        Valor total del inventario (sum de price * stock).

        Returns:
            Valor total en USD
        """
        pass

    def close(self):
        """Cerrar conexión."""
        self.conn.close()


def print_analytics_report(engine: AnalyticsEngine) -> None:
    """Imprimir reporte analítico completo."""
    print("\n" + "="*60)
    print("INVENTORY ANALYTICS REPORT")
    print("="*60)

    # TODO: Mostrar estadísticas por categoría
    # TODO: Mostrar productos con bajo stock
    # TODO: Mostrar valor total de inventario
    # TODO: Mostrar top 3 categorías por valor


if __name__ == "__main__":
    print("Initializing analytics engine...")
    engine = AnalyticsEngine(ANALYTICS_DB)

    print(f"Loading products from {CSV_PATH}...")
    # TODO: Implementar load_products_from_csv

    print_analytics_report(engine)

    engine.close()
    print("\nAnalytics complete!")
