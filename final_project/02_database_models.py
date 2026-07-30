"""
Phase 2: Database Models

Objetivos:
- Definir modelos SQLAlchemy
- Definir modelos Pydantic para API
- Type-safe data structures
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "inventory.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()


# TODO: Definir modelo ORM de Product
class ProductORM(Base):
    """
    Modelo SQLAlchemy para la tabla products.

    Campos:
    - id: Clave primaria (integer, auto-incremento)
    - name: Nombre del producto (string, único, obligatorio)
    - category: Categoría (string, obligatorio)
    - price: Precio en USD (float, > 0)
    - stock: Cantidad en inventario (integer, >= 0)
    - created_at: Fecha de creación (datetime, auto-set)
    """

    __tablename__ = "products"

    # TODO: Definir columnas
    pass


# TODO: Definir modelo Pydantic para crear productos
class ProductCreate(BaseModel):
    """
    Modelo para validar datos al crear un producto.

    Validaciones:
    - name: 1-100 caracteres
    - price: > 0
    - category: obligatorio
    - stock: >= 0 (default 0)
    """

    pass


# TODO: Definir modelo Pydantic para respuestas
class ProductResponse(BaseModel):
    """
    Modelo para respuestas de la API.

    Incluye todos los campos del ProductORM más metadatos.
    """

    pass


# TODO: Crear tablas
def init_database() -> None:
    """Crear todas las tablas en la base de datos."""
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized: {DB_PATH}")


if __name__ == "__main__":
    init_database()

    # Verificar que el modelo funciona
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)

    print("\nDatabase schema created successfully!")
    print(f"Database file: {DB_PATH}")
