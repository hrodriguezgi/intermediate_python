# %% [markdown]
# # 03. Data Validation
#
# ## Objetivos
#
# - Crear modelos Pydantic con validaciones complejas
# - Validadores personalizados
# - Manejo de campos opcionales y por defecto
# - Serialización y respuestas formateadas

# %% [markdown]
# ## Validación básica con Pydantic
#
# Los type hints automáticamente validan tipos.

# %%
from pydantic import BaseModel, Field, validator, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Validación simple: type hints
class SimpleProduct(BaseModel):
    name: str  # Obligatorio, tipo string
    price: float  # Obligatorio, tipo float
    stock: int = 0  # Opcional, default 0


# Esto funciona:
# product = SimpleProduct(name="Laptop", price=999.99, stock=5)

# Esto falla (type error):
# product = SimpleProduct(name="Laptop", price="999.99")  # price debe ser float

# %% [markdown]
# ## Validadores con restricciones
#
# Usar Field() para añadir restricciones más precisas.

# %%
class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    price: float = Field(..., gt=0, le=1000000, description="Precio > 0")
    stock: int = Field(default=0, ge=0, description="Stock >= 0")
    discount: float = Field(default=0, ge=0, le=100, description="Descuento 0-100%")
    weight_kg: Optional[float] = Field(None, ge=0, description="Peso en kg")

    class Config:
        example = {
            "name": "Professional Laptop",
            "price": 1299.99,
            "stock": 5,
            "discount": 10,
            "weight_kg": 1.5
        }


# %% [markdown]
# ## Validadores personalizados
#
# Lógica de validación compleja con @validator.

# %%
class Order(BaseModel):
    order_id: str
    email: str
    quantity: int
    total_price: float

    @validator('order_id')
    def order_id_must_be_uppercase(cls, v):
        if not v.isupper():
            raise ValueError('order_id must be uppercase')
        return v

    @validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('invalid email format')
        return v

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('quantity must be > 0')
        return v

    @validator('total_price')
    def total_price_must_match(cls, v, values):
        # Validación entre campos
        if 'quantity' in values:
            # Podemos acceder a otros campos
            pass
        if v < 0:
            raise ValueError('total_price cannot be negative')
        return v


# %% [markdown]
# ## Enumeraciones para opciones restringidas
#
# Cuando un campo solo puede ser uno de varios valores.

# %%
class CategoryEnum(str, Enum):
    ELECTRONICS = "electronics"
    APPLIANCES = "appliances"
    FURNITURE = "furniture"
    CLOTHING = "clothing"


class ProductWithCategory(BaseModel):
    name: str
    category: CategoryEnum  # Solo acepta los valores del Enum
    price: float


# Funciona:
# p = ProductWithCategory(name="Laptop", category="electronics", price=999.99)

# Falla (valor no válido):
# p = ProductWithCategory(name="Laptop", category="invalid", price=999.99)

# %% [markdown]
# ## Listas y objetos anidados
#
# Validación de estructuras complejas.

# %%
class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price_per_unit: float = Field(..., gt=0)

    def total_price(self) -> float:
        return self.quantity * self.price_per_unit


class ComplexOrder(BaseModel):
    order_id: str
    customer_email: str
    items: List[OrderItem]  # Lista de objetos validados
    shipping_address: str
    notes: Optional[str] = None

    @validator('items')
    def items_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('Order must have at least one item')
        return v

    @property
    def total_amount(self) -> float:
        return sum(item.total_price() for item in self.items)


# %% [markdown]
# ## Validación de rangos y patrones
#
# Restricciones numéricas y de string.

# %%
from pydantic import constr, conint, validator
import re

# constr: string con restricciones
class Account(BaseModel):
    username: constr(min_length=3, max_length=20)  # 3-20 caracteres
    password: constr(min_length=8)  # Mínimo 8 caracteres
    phone: Optional[constr(regex=r'^\+?1?\d{9,15}$')] = None  # Formato de teléfono


# %% [markdown]
# ## Alias de campos
#
# Mapear nombres de JSON a nombres de Python.

# %%
class ProductFromExternalAPI(BaseModel):
    id: int
    productName: str  # En JSON es 'productName'
    priceUSD: float  # En JSON es 'priceUSD'

    class Config:
        # Usar 'allow_population_by_field_name' para aceptar ambos nombres
        populate_by_name = True  # Pydantic 2.0
        # fields = {
        #     'productName': {'alias': 'product_name'},  # Antiguo
        # }


# %% [markdown]
# ## Transformaciones: normalizar datos
#
# Limpiar y normalizar datos en validadores.

# %%
class NormalizedProduct(BaseModel):
    name: str
    description: str

    @validator('name')
    def normalize_name(cls, v):
        # Limpiar espacios y convertir a título
        return v.strip().title()

    @validator('description')
    def normalize_description(cls, v):
        # Asegurarse de que descripciones tengan formato
        return v.strip().capitalize()


# Prueba:
# p = NormalizedProduct(name="  laptop computer  ", description="high performance laptop")
# # name = "Laptop Computer"
# # description = "High performance laptop"

# %% [markdown]
# ## Validación cruzada: depende de otros campos
#
# Cuando una validación depende de múltiples campos.

# %%
class PriceRange(BaseModel):
    min_price: float
    max_price: float

    @validator('max_price')
    def max_greater_than_min(cls, v, values):
        if 'min_price' in values and v <= values['min_price']:
            raise ValueError('max_price must be greater than min_price')
        return v


# %% [markdown]
# ## Modelos con relaciones opcionales
#
# Algunos campos dependen de otros.

# %%
class DiscountCode(BaseModel):
    code: str
    discount_percent: float = Field(..., ge=0, le=100)
    valid_from: datetime
    valid_until: datetime

    @validator('valid_until')
    def valid_until_after_from(cls, v, values):
        if 'valid_from' in values and v <= values['valid_from']:
            raise ValueError('valid_until must be after valid_from')
        return v


# %% [markdown]
# ## Respuestas personalizadas
#
# Controlar cómo se serializa la respuesta.

# %%
class UserPublic(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        # No exponemos password, last_login, etc.
        # Solo los campos definidos en el modelo
        from_attributes = True


class UserPrivate(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_admin: bool = False

    class Config:
        from_attributes = True


# %% [markdown]
# ## Validación en FastAPI: todo junto
#
# Cómo se ve en una aplicación real.

# %%
from fastapi import FastAPI, HTTPException, Body
from typing import Annotated

app = FastAPI()


@app.post("/orders", status_code=201)
async def create_order(
    order: Annotated[ComplexOrder, Body(..., example={
        "order_id": "ORD-001",
        "customer_email": "customer@example.com",
        "items": [
            {"product_id": 1, "quantity": 2, "price_per_unit": 99.99},
            {"product_id": 2, "quantity": 1, "price_per_unit": 49.99}
        ],
        "shipping_address": "123 Main St, City, State",
        "notes": "Please deliver in the morning"
    })]
):
    """
    Crear una orden.

    FastAPI automáticamente:
    1. Valida que 'items' sea lista de OrderItem
    2. Valida que cada item tenga quantity > 0
    3. Valida que la lista no esté vacía
    4. Devuelve errores claros si algo falla
    """
    return {
        "order_id": order.order_id,
        "total_amount": order.total_amount,
        "status": "confirmed"
    }


# %% [markdown]
# ## Manejo de errores de validación
#
# FastAPI devuelve errores de Pydantic automáticamente como 422.

# %%
# Si el usuario envía esto (cantidad negativa):
# POST /orders
# {
#     "order_id": "ORD-001",
#     "customer_email": "customer@example.com",
#     "items": [{"product_id": 1, "quantity": -5, "price_per_unit": 99.99}],
#     "shipping_address": "123 Main St"
# }
#
# FastAPI responde:
# 422 Unprocessable Entity
# {
#     "detail": [
#         {
#             "loc": ["body", "items", 0, "quantity"],
#             "msg": "ensure this value is greater than 0",
#             "type": "value_error.number.not_gt"
#         }
#     ]
# }

# %% [markdown]
# ## Resumen
#
# - **Type hints:** Validación automática de tipos
# - **Field():** Restricciones (min/max, regex, etc.)
# - **@validator:** Lógica de validación personalizada
# - **Enums:** Campos con opciones limitadas
# - **Nested models:** Objetos complejos validados
# - **Errores:** FastAPI devuelve errores 422 automáticamente
# - **Transformaciones:** Normalizar datos en validadores
#
# Ahora tienes validación robusta para tu API.
# Próximo: Final project - aplicar todo lo aprendido.
