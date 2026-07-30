"""
Phase 3: SQLite Operations

Objetivos:
- Insertar datos con transacciones
- Manejar errores (duplicados, constraint violations)
- Queries básicas
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Import models from Phase 2
from typing import List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "inventory.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# TODO: Implementar función de inserción en lote
def insert_products_batch(
    session: Session,
    products: List[Dict[str, Any]],
    batch_size: int = 100
) -> Dict[str, int]:
    """
    Insertar productos en lotes con manejo de errores.

    Debe:
    1. Procesar en lotes de batch_size
    2. Manejar IntegrityError (duplicados)
    3. Registrar cuántos se insertaron vs. fallaron
    4. Hacer commit por lote

    Args:
        session: Sesión SQLAlchemy
        products: Lista de dicts con datos de productos
        batch_size: Tamaño del lote

    Returns:
        Dict con {"inserted": N, "failed": N}
    """
    pass  # TODO


# TODO: Implementar función para obtener todos
def get_all_products(session: Session) -> List[Any]:
    """
    Obtener todos los productos de la base de datos.

    Returns:
        Lista de objetos ProductORM
    """
    pass  # TODO


# TODO: Implementar función para buscar por ID
def get_product_by_id(session: Session, product_id: int) -> Any:
    """
    Obtener un producto por ID.

    Args:
        session: Sesión SQLAlchemy
        product_id: ID a buscar

    Returns:
        ProductORM o None si no existe
    """
    pass  # TODO


# TODO: Implementar función para actualizar stock
def update_product_stock(session: Session, product_id: int, new_stock: int) -> bool:
    """
    Actualizar el stock de un producto.

    Debe verificar que new_stock >= 0.

    Args:
        session: Sesión SQLAlchemy
        product_id: ID del producto
        new_stock: Nuevo valor de stock

    Returns:
        True si éxito, False si producto no existe
    """
    pass  # TODO


# TODO: Implementar función transaccional de venta
def sell_product(session: Session, product_id: int, quantity: int) -> Dict[str, Any]:
    """
    Realizar una venta (restar del stock) de forma transaccional.

    Debe:
    1. Verificar que el producto existe
    2. Verificar que hay stock suficiente
    3. Actualizar stock
    4. Hacer commit
    5. Retornar información de la venta

    Args:
        session: Sesión SQLAlchemy
        product_id: ID del producto
        quantity: Cantidad a vender

    Returns:
        Dict con {"product_name": ..., "quantity_sold": ..., "new_stock": ...}

    Raises:
        ValueError: Si no hay stock o producto no existe
    """
    pass  # TODO


if __name__ == "__main__":
    # Load data from Phase 1
    from path import load_products_csv

    print("Loading products from CSV...")
    # TODO: Cargar CSV usando la función de Phase 1

    print("\nInserting into SQLite...")
    # TODO: Usar insert_products_batch

    print("\nVerifying data...")
    # TODO: Usar get_all_products para verificar

    print("\nTesting operations...")
    # TODO: Probar get_product_by_id, update_product_stock, sell_product
