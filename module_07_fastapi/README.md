# Module 7 · FastAPI

Construir APIs REST modernas con validación automática y documentación.

## Lecciones

### 01. FastAPI Basics
**Temas:** Endpoints, type hints, validación automática
- ¿Qué es FastAPI?
- GET, POST, PUT, DELETE endpoints
- Type hints = validación + documentación
- Modelos Pydantic
- Swagger UI automática

**Aprendes:** Crear API REST moderna en minutos

### 02. Database Integration
**Temas:** Conectar a bases de datos, CRUD completo
- Dependency injection para sesiones
- Conectar a SQLite desde FastAPI
- Implementar CRUD operations
- Error handling (404, 400, 409, etc.)
- Transacciones vía API
- Endpoint analítico

**Aprendes:** API conectada a base de datos real

### 03. Data Validation
**Temas:** Pydantic avanzado, validadores, serialización
- Validadores personalizados
- Restricciones numéricas y de string
- Validación cruzada entre campos
- Enumeraciones para opciones
- Nested models
- Transformación de datos
- Errores de validación automáticos

**Aprendes:** Validar datos robustamente

## Ejercicios

No hay ejercicios individuales - todo aplicado en el Proyecto Final.

## Proyecto Final

Ver `final_project/` en la raíz del curso:
- `05_fastapi_application.py` es el culminar del módulo
- API CRUD + Analytics + Transacciones

## Ejecutar

```bash
# Lesson 1: API básica
python -m module_07_fastapi.01_fastapi_basics
# No arranca servidor (solo demostración)

# Lesson 2: Conectada a base de datos
uvicorn module_07_fastapi.02_database_integration:app --reload

# Lesson 3: Validación
python -m module_07_fastapi.03_data_validation
# No arranca servidor (solo demostración)

# Proyecto Final: API completa
cd final_project
uvicorn 05_fastapi_application:app --reload
```

Luego visita: `http://localhost:8000/docs`

## Concepto Clave

**Type Hints = Automatic Everything**

```python
@app.post("/products")
async def create_product(product: ProductCreate):
    # ProductCreate se valida automáticamente
    # Swagger UI genera schema automáticamente
    # Errores 422 con detalles automáticos
    return product
```

## Swagger UI

Cuando la API corre, visita `http://localhost:8000/docs`:
- Documentación interactiva
- Prueba endpoints directamente
- Ejemplos de request/response
- Schema automático

## Requisitos

```
fastapi>=0.100
uvicorn[standard]>=0.24
pydantic>=2.0
sqlalchemy>=2.0
```

## Patrón: Dependency Injection

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products")
async def list_products(db: Session = Depends(get_db)):
    # db es automáticamente inyectado y limpiado
    pass
```

## Patrón: Validación

```python
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

# Automáticamente:
# - name no vacío
# - price > 0
# - Devuelve 422 si falla
```

## HTTP Status Codes

| Code | Significado | Cuándo usar |
|------|------------|-----------|
| 200 | OK | GET/PUT/PATCH éxito |
| 201 | Created | POST éxito |
| 204 | No Content | DELETE éxito |
| 400 | Bad Request | Datos inválidos del cliente |
| 404 | Not Found | Recurso no existe |
| 409 | Conflict | Violación de constraint |
| 422 | Unprocessable Entity | Validación fallida |
| 500 | Server Error | Error inesperado |

## Siguiente

 Final Project: Aplicar todo lo aprendido en una aplicación completa
