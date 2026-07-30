# %% [markdown]
# # 01. FastAPI Basics
#
# ## Objetivos
#
# - Crear endpoints HTTP (GET, POST)
# - Usar type hints para documentar API automáticamente
# - Validar datos con Pydantic
# - Entender request y response models

# %% [markdown]
# ## ¿Qué es FastAPI?
#
# FastAPI es un framework moderno para construir APIs REST en Python.
#
# ```python
# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}
# ```
#
# **Ventajas:**
# - Type hints = validación automática + documentación
# - Muy rápido (async/await)
# - Genera OpenAPI (Swagger) automáticamente
# - Errores claros

# %% [markdown]
# ## Instalación
#
# ```bash
# pip install fastapi uvicorn[standard]
# ```
#
# Uvicorn es el servidor ASGI que ejecuta FastAPI.

# %%
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="Product Inventory API",
    description="API para gestionar inventario de productos",
    version="1.0.0"
)

# %% [markdown]
# ## Definir modelos con Pydantic
#
# Los modelos definen la estructura de datos y validan automáticamente.

# %%
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    price: float = Field(..., gt=0, description="Precio debe ser > 0")
    category: str = Field(..., description="Categoría del producto")
    stock: int = Field(default=0, ge=0, description="Stock disponible")

    class Config:
        example = {
            "name": "Laptop",
            "price": 999.99,
            "category": "Electronics",
            "stock": 10
        }


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str
    stock: int
    created_at: datetime

    class Config:
        from_attributes = True  # Para convertir de ORM a Pydantic


# %% [markdown]
# ## Endpoint GET simple
#
# Devolver datos de forma simple.

# %%
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Product Inventory API"}


# %% [markdown]
# ## GET con parámetro en ruta
#
# `/products/{product_id}` - el `{product_id}` es un parámetro.

# %%
# Simulamos una base de datos en memoria para este ejemplo
fake_products_db = {
    1: {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "category": "Electronics",
        "stock": 5,
        "created_at": datetime.now()
    },
    2: {
        "id": 2,
        "name": "Mouse",
        "price": 25.99,
        "category": "Accessories",
        "stock": 100,
        "created_at": datetime.now()
    }
}


@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def get_product(product_id: int):
    """
    Obtener un producto por ID.

    - **product_id**: ID del producto (debe existir)
    """
    if product_id not in fake_products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    return fake_products_db[product_id]


# %% [markdown]
# ## GET con parámetros query
#
# `/products?category=Electronics&min_price=100`

# %%
@app.get("/products", response_model=List[ProductResponse], tags=["Products"])
async def list_products(
    category: Optional[str] = None,
    min_price: float = 0,
    max_price: float = 999999,
    skip: int = 0,
    limit: int = 10
):
    """
    Listar productos con filtros opcionales.

    - **category**: Filtrar por categoría (opcional)
    - **min_price**: Precio mínimo (default 0)
    - **max_price**: Precio máximo (default 999999)
    - **skip**: Saltar N resultados (paginación)
    - **limit**: Limitar a N resultados (default 10)
    """
    results = []

    for product in fake_products_db.values():
        # Aplicar filtros
        if category and product["category"] != category:
            continue

        if not (min_price <= product["price"] <= max_price):
            continue

        results.append(product)

    # Paginación simple
    return results[skip : skip + limit]


# %% [markdown]
# ## POST: crear recursos
#
# Enviar datos al servidor para crear algo.

# %%
@app.post("/products", response_model=ProductResponse, status_code=201, tags=["Products"])
async def create_product(product: ProductCreate):
    """
    Crear un nuevo producto.

    El servidor automáticamente:
    - Valida que 'name', 'price', 'category' cumplan reglas (Pydantic)
    - Asigna un ID
    - Devuelve el producto creado con status 201
    """
    # Generar nuevo ID
    new_id = max(fake_products_db.keys()) + 1 if fake_products_db else 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "stock": product.stock,
        "created_at": datetime.now()
    }

    fake_products_db[new_id] = new_product
    return new_product


# %% [markdown]
# ## PUT: actualizar recursos
#
# Reemplazar un recurso completamente.

# %%
@app.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def update_product(product_id: int, product: ProductCreate):
    """
    Actualizar un producto existente.

    Reemplaza TODOS los campos del producto.
    """
    if product_id not in fake_products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    updated = {
        "id": product_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "stock": product.stock,
        "created_at": fake_products_db[product_id]["created_at"]  # Mantener fecha original
    }

    fake_products_db[product_id] = updated
    return updated


# %% [markdown]
# ## DELETE: eliminar recursos
#
# Borrar un recurso por ID.

# %%
@app.delete("/products/{product_id}", status_code=204, tags=["Products"])
async def delete_product(product_id: int):
    """
    Eliminar un producto por ID.

    Devuelve status 204 (sin contenido) si éxito.
    """
    if product_id not in fake_products_db:
        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    del fake_products_db[product_id]
    return None


# %% [markdown]
# ## Type hints = documentación automática
#
# FastAPI genera OpenAPI (Swagger UI) automáticamente.
#
# Visita: http://localhost:8000/docs
#
# Todos los parámetros, tipos, ejemplos aparecen automáticamente.

# %% [markdown]
# ## Ejecutar el servidor
#
# ```bash
# uvicorn 01_fastapi_basics:app --reload
# ```
#
# El `--reload` recarga el servidor cuando cambias el código.
#
# Ahora puedes:
# - Visitar http://localhost:8000/docs (Swagger UI)
# - Hacer requests: `curl http://localhost:8000/products/1`

# %% [markdown]
# ## Resumen
#
# - **@app.get()**: Endpoints que leen datos (safe, idempotent)
# - **@app.post()**: Endpoints que crean datos (status 201)
# - **@app.put()**: Endpoints que actualizan datos (reemplazar)
# - **@app.delete()**: Endpoints que eliminan datos (status 204)
# - **Pydantic models**: Validan datos automáticamente
# - **Type hints**: Documentación y validación integradas
#
# Próximo: Conectar FastAPI a bases de datos reales (SQLite/DuckDB).
