# %% [markdown]
# # 02. Database Integration
#
# ## Objetivos
#
# - Conectar FastAPI a SQLite (datos transaccionales)
# - Conectar FastAPI a DuckDB (datos analíticos)
# - Usar dependency injection para sesiones
# - Implementar CRUD operations via API
# - Manejo de errores HTTP

# %% [markdown]
# ## Patrón: Dependency Injection
#
# FastAPI permite inyectar dependencias automáticamente en endpoints.
#
# Esto es útil para sesiones de base de datos.

# %%
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "api.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="Inventory API with Database",
    description="API conectada a base de datos real",
    version="2.0.0"
)

# %% [markdown]
# ## Modelo ORM (SQLAlchemy)
#
# Define la estructura de datos en la base de datos.

# %%
class ProductORM(Base):
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), unique=True, nullable=False)
    description: str = Column(String(500), nullable=True)
    price: float = Column(Float, nullable=False)
    stock: int = Column(Integer, default=0)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price=${self.price})>"


Base.metadata.create_all(bind=engine)

# %% [markdown]
# ## Modelos Pydantic (validación HTTP)
#
# Define lo que viene en requests y va en responses.

# %%
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    created_at: datetime

    class Config:
        from_attributes = True  # Convierte ORM a Pydantic


# %% [markdown]
# ## Dependency Injection: Database Session
#
# Cada request obtiene una sesión automáticamente.

# %%
def get_db():
    """
    Dependency que proporciona una sesión de base de datos.

    Se cierra automáticamente después del request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# %% [markdown]
# ## GET: Listar todos los productos

# %%
@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
async def list_products(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Listar productos con paginación.

    - **skip**: Saltar N productos
    - **limit**: Máximo de productos a devolver
    """
    products = db.query(ProductORM).offset(skip).limit(limit).all()
    return products


# %% [markdown]
# ## GET: Obtener un producto por ID

# %%
@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtener un producto específico por ID.

    Devuelve 404 si no existe.
    """
    product = db.query(ProductORM).filter(ProductORM.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    return product


# %% [markdown]
# ## GET: Búsqueda por nombre

# %%
@app.get("/products/search/{query}", response_model=List[ProductResponse], tags=["Products"])
async def search_products(
    query: str,
    db: Session = Depends(get_db)
):
    """
    Buscar productos que contengan el query en el nombre.

    Case-insensitive.
    """
    products = db.query(ProductORM).filter(
        ProductORM.name.ilike(f"%{query}%")
    ).all()

    return products


# %% [markdown]
# ## POST: Crear un producto
#
# Valida datos, maneja duplicados con IntegrityError.

# %%
@app.post("/products", response_model=ProductResponse, status_code=201, tags=["Products"])
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo producto.

    Devuelve 201 si éxito, 400 si hay error de validación.
    """
    try:
        db_product = ProductORM(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(
                status_code=400,
                detail=f"Product '{product.name}' already exists"
            )
        raise HTTPException(
            status_code=400,
            detail="Database error"
        )


# %% [markdown]
# ## PUT: Actualizar un producto
#
# Solo actualiza los campos que se envíen.

# %%
@app.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un producto.

    Solo actualiza los campos enviados (partial update).
    """
    db_product = db.query(ProductORM).filter(ProductORM.id == product_id).first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    try:
        update_data = product_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Product name already exists"
        )


# %% [markdown]
# ## DELETE: Eliminar un producto

# %%
@app.delete("/products/{product_id}", status_code=204, tags=["Products"])
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un producto por ID.

    Devuelve 204 si éxito, 404 si no existe.
    """
    db_product = db.query(ProductORM).filter(ProductORM.id == product_id).first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    db.delete(db_product)
    db.commit()
    return None


# %% [markdown]
# ## Endpoint analítico: Estadísticas de inventario
#
# Usa funciones de agregación SQL para análisis.

# %%
from sqlalchemy import func

class InventoryStats(BaseModel):
    total_products: int
    total_value: float
    average_price: float
    low_stock_count: int  # Productos con stock < 5


@app.get("/analytics/inventory", response_model=InventoryStats, tags=["Analytics"])
async def inventory_stats(db: Session = Depends(get_db)):
    """
    Estadísticas rápidas del inventario.

    Usa funciones SQL de agregación para cálculos rápidos.
    """
    total_products = db.query(func.count(ProductORM.id)).scalar()
    total_value = db.query(func.sum(ProductORM.price * ProductORM.stock)).scalar() or 0.0
    average_price = db.query(func.avg(ProductORM.price)).scalar() or 0.0
    low_stock = db.query(func.count(ProductORM.id)).filter(ProductORM.stock < 5).scalar()

    return {
        "total_products": total_products or 0,
        "total_value": total_value,
        "average_price": average_price,
        "low_stock_count": low_stock
    }


# %% [markdown]
# ## Transacción: Vender producto
#
# Múltiples cambios que deben ser atómicos (todo o nada).

# %%
class SaleRequest(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class SaleResponse(BaseModel):
    product_name: str
    quantity_sold: int
    new_stock: int
    total_price: float


@app.post("/sales", response_model=SaleResponse, tags=["Sales"])
async def sell_product(
    sale: SaleRequest,
    db: Session = Depends(get_db)
):
    """
    Vender una cantidad de un producto.

    Actualiza stock en una transacción atómica.
    """
    try:
        product = db.query(ProductORM).filter(ProductORM.id == sale.product_id).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {sale.product_id} not found"
            )

        if product.stock < sale.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock: {product.stock} available, {sale.quantity} requested"
            )

        # Actualizar stock
        product.stock -= sale.quantity
        db.commit()
        db.refresh(product)

        return {
            "product_name": product.name,
            "quantity_sold": sale.quantity,
            "new_stock": product.stock,
            "total_price": product.price * sale.quantity
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Sale failed: {str(e)}"
        )


# %% [markdown]
# ## Resumen
#
# - **Dependency Injection:** `Depends(get_db)` proporciona sesión automáticamente
# - **CRUD completo:** Create, Read, Update, Delete vía HTTP
# - **Validación:** Pydantic valida input, ORM maneja persistencia
# - **Errores claros:** HTTPException mapea errores a status codes
# - **Transacciones:** Múltiples cambios se hacen juntos (atomicity)
#
# Próximo: Validación y errores más avanzados.
