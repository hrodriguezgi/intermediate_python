"""
Phase 5: FastAPI Application

Objetivos:
- Crear API REST completa
- Conectar a SQLite
- Validación con Pydantic
- Errores HTTP apropiados

Para correr:
    uvicorn 05_fastapi_application:app --reload

Visitar: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path

# TODO: Import models de Phase 2
# TODO: Import database connection

app = FastAPI(
    title="Inventory Management API",
    description="API para gestionar inventario de productos",
    version="1.0.0"
)


# TODO: Implementar dependency para sesión
def get_db():
    """Proporcionar sesión de base de datos."""
    pass


# ============================================================================
# ENDPOINTS DE LECTURA (GET)
# ============================================================================

# TODO: GET /products - Listar productos con paginación
@app.get("/products", tags=["Products"])
async def list_products(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Listar productos con filtros opcionales.

    Query parameters:
    - skip: Saltar N productos (paginación)
    - limit: Máximo de productos (default 10)
    - category: Filtrar por categoría

    Returns:
        Lista de productos
    """
    pass


# TODO: GET /products/{product_id} - Obtener un producto
@app.get("/products/{product_id}", tags=["Products"])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtener un producto por ID.

    Returns:
        Producto completo o 404 si no existe
    """
    pass


# TODO: GET /analytics/summary - Resumen de inventario
@app.get("/analytics/summary", tags=["Analytics"])
async def inventory_summary(db: Session = Depends(get_db)):
    """
    Resumen del inventario.

    Returns:
        {
            "total_products": N,
            "total_value": $,
            "average_price": $,
            "low_stock_count": N
        }
    """
    pass


# ============================================================================
# ENDPOINTS DE ESCRITURA (POST, PUT, DELETE)
# ============================================================================

# TODO: POST /products - Crear un producto
@app.post("/products", status_code=201, tags=["Products"])
async def create_product(
    product: "ProductCreate",  # TODO: Import ProductCreate from Phase 2
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo producto.

    Validaciones automáticas:
    - name es único
    - price > 0
    - stock >= 0

    Returns:
        Producto creado (201)
        Error si ya existe (400)
    """
    pass


# TODO: PUT /products/{product_id} - Actualizar un producto
@app.put("/products/{product_id}", tags=["Products"])
async def update_product(
    product_id: int,
    product_update: "ProductUpdate",  # TODO: Crear modelo ProductUpdate
    db: Session = Depends(get_db)
):
    """
    Actualizar un producto.

    Actualiza solo los campos enviados (partial update).

    Returns:
        Producto actualizado
        404 si no existe
    """
    pass


# TODO: DELETE /products/{product_id} - Eliminar un producto
@app.delete("/products/{product_id}", status_code=204, tags=["Products"])
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un producto.

    Returns:
        204 si éxito
        404 si no existe
    """
    pass


# ============================================================================
# ENDPOINT TRANSACCIONAL
# ============================================================================

# TODO: POST /sales - Realizar una venta
@app.post("/sales", tags=["Sales"])
async def record_sale(
    sale: "SaleRequest",  # TODO: Crear modelo SaleRequest
    db: Session = Depends(get_db)
):
    """
    Registrar una venta (reduce stock).

    Request:
        {
            "product_id": 1,
            "quantity": 5
        }

    Returns:
        {
            "product_name": "Laptop",
            "quantity_sold": 5,
            "new_stock": 10,
            "total_price": $999.95
        }

    Errores:
        400 - Cantidad insuficiente
        404 - Producto no existe
    """
    pass


# ============================================================================
# UTILS
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz."""
    return {"message": "Welcome to Inventory Management API"}


@app.get("/health", tags=["Health"])
async def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    print("Starting Inventory Management API...")
    print("Visit http://localhost:8000/docs for Swagger UI")

    uvicorn.run(app, host="0.0.0.0", port=8000)
