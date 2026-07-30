# %% [markdown]
# # 01. SQLAlchemy Fundamentals
#
# ## Objetivos
#
# - Entender qué es un ORM (Object-Relational Mapping)
# - Definir modelos de datos con SQLAlchemy
# - Crear, leer, actualizar datos con sesiones
# - Escribir queries tipo SQL desde Python

# %% [markdown]
# ## ¿Por qué SQLAlchemy?
#
# Sin ORM, trabajas con SQL directo:
# ```python
# cursor.execute("SELECT * FROM products WHERE price > ?", (50,))
# rows = cursor.fetchall()
# # Tienes que convertir manualmente a Python objects
# ```
#
# Con SQLAlchemy:
# ```python
# products = session.query(Product).filter(Product.price > 50).all()
# # Ya tienes objetos Python, no tuples
# ```
#
# **Ventaja:** Seguridad (sin SQL injection), claridad (el código es Python, no strings),
# y reutilización (cambiar de SQLite a PostgreSQL sin reescribir queries).

# %%
from dataclasses import dataclass
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "products.db"
DB_URL = f"sqlite:///{DB_PATH}"

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False)
    price: float = Column(Float, nullable=False)
    category: str = Column(String(50), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price=${self.price:.2f})>"


# %% [markdown]
# ## Creando la base de datos
#
# Una vez tenemos el modelo, SQLAlchemy puede crear todas las tablas automáticamente.

# %%
engine = create_engine(DB_URL, echo=False)
Base.metadata.create_all(engine)

print(f"Database created at: {DB_PATH}")
print(f"Database exists: {DB_PATH.exists()}")

# %% [markdown]
# ## Insertando datos con sesión
#
# Las sesiones son conexiones reutilizables que manejan transacciones automáticamente.

# %%
session = Session(engine)

products = [
    Product(name="Laptop", price=999.99, category="Electronics"),
    Product(name="Coffee Maker", price=49.99, category="Appliances"),
    Product(name="Desk Lamp", price=29.99, category="Furniture"),
]

session.add_all(products)
session.commit()

print("Products inserted successfully")

# %% [markdown]
# ## Leyendo datos
#
# Queries en SQLAlchemy se ven como Python.

# %%
all_products = session.query(Product).all()
print(f"Total products: {len(all_products)}")
for p in all_products:
    print(p)

# %% [markdown]
# ## Filtros y búsquedas
#
# Búsquedas específicas con filter().

# %%
# Productos caros (> $50)
expensive = session.query(Product).filter(Product.price > 50).all()
print(f"\nExpensive products (>$50):")
for p in expensive:
    print(f"  {p.name}: ${p.price:.2f}")

# %% [markdown]
# ## Actualizando datos
#
# Modificar objetos y commit() persiste los cambios.

# %%
laptop = session.query(Product).filter(Product.name == "Laptop").first()
print(f"\nBefore update: {laptop}")

laptop.price = 899.99
session.commit()

print(f"After update: {laptop}")

# %% [markdown]
# ## Eliminando datos
#
# Delete y commit para remover registros.

# %%
lamp = session.query(Product).filter(Product.name == "Desk Lamp").first()
session.delete(lamp)
session.commit()

print(f"\nProducts after deletion: {len(session.query(Product).all())}")

# %% [markdown]
# ## Queries más complejas
#
# Ordenar, limitar, contar.

# %%
# Contar total
total = session.query(Product).count()
print(f"Total products: {total}")

# Top N más caros
top_expensive = session.query(Product).order_by(Product.price.desc()).limit(2).all()
print(f"\nTop 2 most expensive:")
for p in top_expensive:
    print(f"  {p.name}: ${p.price:.2f}")

# %% [markdown]
# ## Context Manager (Recomendado)
#
# Usar `with` automáticamente cierra la sesión. Mejor para código limpio.

# %%
with Session(engine) as session:
    products_in_context = session.query(Product).all()
    print(f"\nProducts (usando context manager): {len(products_in_context)}")

# La sesión se cierra automáticamente aquí

# %% [markdown]
# ## Nota: Type Hints Modernos
#
# SQLAlchemy 2.0+ tiene soporte para type hints, pero requiere Mapped[] de typing
# para máxima type-safety. El patrón actual funciona bien para la mayoría de casos.


# %% [markdown]
# ## Resumen
#
# - **ORM:** Convierte SQL a objetos Python automáticamente
# - **Modelos:** Definen la estructura de datos y tabla
# - **Sesiones:** Manejan transacciones y cambios a datos
# - **Queries:** Se escriben en Python, no en SQL strings
# - **Seguridad:** Sin SQL injection, parámetros automáticos
#
# Próximo: Usaremos esto en SQLite con transacciones y manejo de errores.

# %%
session.close()
