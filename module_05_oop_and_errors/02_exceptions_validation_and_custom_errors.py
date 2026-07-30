# %% [markdown]
# # 02. Excepciones y validación
#
# ## Objetivos
#
# - Fallar con mensajes útiles.
# - Crear excepciones específicas cuando aporta claridad.

# %%
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Protocol


class EnrollmentError(Exception):
    pass


def enroll_student(student_name: str, seats_left: int) -> str:
    if not student_name.strip():
        raise EnrollmentError("student_name cannot be empty")
    if seats_left <= 0:
        raise EnrollmentError("no seats available")
    return f"{student_name} enrolled"


try:
    print(enroll_student("Ana", 2))
    print(enroll_student("", 1))
except EnrollmentError as error:
    print("Enrollment failed:", error)

# %%
try:
    print(enroll_student("Ana", 0))
except EnrollmentError as error:
    print("Enrollment failed:", error)

# %% [markdown]
# ## Excepciones con Contexto
#
# ### El Problema: Excepciones genéricas no ayudan
#
# Cuando procesas datos reales (filas de CSV, registros de API), necesitas saber
# qué campo falló, qué valor era, por qué falló. Las excepciones simples no dan contexto.


# %%
# Versión simple: no es útil en debugging
class SimpleError(Exception):
    pass


def validate_row_simple(row: dict) -> bool:
    if not isinstance(row.get("age"), int):
        raise SimpleError("Invalid data")  # ¿Qué campo? ¿Qué valor?
    return True


# Cuando esto falla en línea 1000 de un CSV grande, no sabes dónde buscar.

# %% [markdown]
# ### La Solución: Excepciones con Contexto


# %%
class DataValidationError(ValueError):
    """Excepción con contexto para validación de datos."""

    def __init__(self, field: str, value: object, reason: str, row_num: int | None = None):
        self.field = field
        self.value = value
        self.reason = reason
        self.row_num = row_num

        location = f" (row {row_num})" if row_num else ""
        message = f"Validation failed{location}: {field}={value!r} - {reason}"
        super().__init__(message)


def validate_row(row: dict, row_num: int | None = None) -> bool:
    if row.get("name") is None or not isinstance(row["name"], str):
        raise DataValidationError(
            field="name",
            value=row.get("name"),
            reason="expected non-empty string",
            row_num=row_num,
        )

    age = row.get("age")
    if not isinstance(age, int):
        raise DataValidationError(
            field="age",
            value=age,
            reason=f"expected int, got {type(age).__name__}",
            row_num=row_num,
        )
    if age < 0:
        raise DataValidationError(
            field="age",
            value=age,
            reason="expected non-negative",
            row_num=row_num,
        )

    return True


# %% [markdown]
# ### En Práctica: CSV con Errores Claros

# %%
rows = [
    {"name": "Ana", "age": 28},
    {"name": "Luis", "age": "30"},  # Error: string en lugar de int
    {"name": None, "age": 25},  # Error: name es None
]

for i, row in enumerate(rows, 1):
    try:
        validate_row(row, row_num=i)
        print(f"Row {i}:  Valid")
    except DataValidationError as e:
        print(f"Row {i}:  {e}")
        print(f"  Field: {e.field}, Value: {e.value}, Reason: {e.reason}")

# %% [markdown]
# ## Elegir la Excepción Correcta
#
# Diferentes problemas merecen diferentes tipos de excepciones.


# %%
# ValueError: entrada del usuario/datos inválida (no el tipo correcto)
def process_count(value: str) -> int:
    try:
        count = int(value)
        if count < 0:
            raise ValueError("count must be non-negative")
        return count
    except ValueError as e:
        raise ValueError(f"cannot convert {value!r} to integer") from e


# TypeError: error de programación (tipo completamente equivocado)
def process_with_callback(data: list, callback: Callable[[object], object] | None = None) -> list:
    if callback is not None and not callable(callback):
        raise TypeError(f"callback must be callable, got {type(callback).__name__}")
    return [callback(x) if callback else x for x in data]


# Excepciones personalizadas: violación de lógica de negocio
class InsufficientFundsError(Exception):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient funds: balance={balance}, requested={amount}")


def transfer_funds(balance: float, amount: float) -> float:
    if balance < amount:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


# %%
# RuntimeError: algo que nunca debería pasar (indica un bug)
def process_state(state: str) -> str:
    if state not in ["open", "closed", "pending"]:
        raise RuntimeError(f"Invalid state: {state!r}")
    return state


# %% [markdown]
# ### Cuándo Usar Cada Una
#
# | Excepción | Cuándo | Ejemplo |
# |-----------|--------|---------|
# | `ValueError` | Entrada inválida del usuario | CSV con campo no-int |
# | `TypeError` | Tipo completamente equivocado | Función espera int, recibe dict |
# | Personalizada | Violación de lógica de negocio | Balance insuficiente |
# | `RuntimeError` | Nunca debería pasar (bug) | Estado desconocido |

# %% [markdown]
# ## Protocol Types (Interfaces sin Herencia)
#
# ### El Problema: Heredar solo para compartir una interfaz

# %%
# Sin Protocol: necesitas heredar de una clase base


class LoaderBase(ABC):
    """Clase base solo para definir interfaz."""

    @abstractmethod
    def load(self) -> dict:
        pass


class CSVLoader(LoaderBase):
    """Debe heredar explícitamente para ser "compatible"."""

    def load(self) -> dict:
        return {"rows": 100, "file": "data.csv"}


class APILoader(LoaderBase):
    """También debe heredar."""

    def load(self) -> dict:
        return {"items": 50, "api": "https://api.example.com"}


# %% [markdown]
# ### La Solución: Protocol - "Duck Typing con Type Hints"
#
# Protocol dice: "Si un objeto tiene estos métodos, lo considero compatible,
# sin necesidad de herencia explícita."


# %%
# Con Protocol: no necesitas heredar, solo tener los métodos correctos
class DataLoader(Protocol):
    """'Contrato' - cualquier objeto con método load() es un DataLoader."""

    def load(self) -> dict:
        """Este método debe existir en objetos que usen Protocol."""
        ...


# Estas clases NO heredan de nada, pero Python las ve como DataLoader
class SimpleCSVLoader:
    """Sin herencia, pero tiene el método load()."""

    def load(self) -> dict:
        print("Leyendo archivo CSV...")
        return {"rows": 1000, "columns": 5}


class DatabaseLoader:
    """Totalmente diferente, pero también tiene load()."""

    def load(self) -> dict:
        print("Consultando base de datos...")
        return {"records": 500, "tables": 3}


class JSONFileLoader:
    """Otro tipo más, con el mismo método."""

    def load(self) -> dict:
        print("Parsando JSON...")
        return {"objects": 200, "nested": True}


# %% [markdown]
# ### Usando Protocol: Función que acepta cualquier "cargador"


# %%
def process_data(loader: DataLoader) -> None:
    """Acepta CUALQUIER objeto que tenga método load()."""
    print("\n--- Procesando datos ---")
    data = loader.load()
    print(f" Datos cargados: {len(data)} items")
    print(f"  Contenido: {data}\n")


# Protocol funciona sin herencia explícita - "duck typing"
print("Ejemplo 1: CSV")
csv_loader = SimpleCSVLoader()
process_data(csv_loader)

print("Ejemplo 2: Base de datos")
db_loader = DatabaseLoader()
process_data(db_loader)

print("Ejemplo 3: JSON")
json_loader = JSONFileLoader()
process_data(json_loader)

# %% [markdown]
# ### Ejemplo Real: Sistema de Almacenamiento Flexible
#
# Imagina que tienes diferentes formas de guardar datos.
# Con Protocol, tu código no necesita saber cuál es.


# %%
class FileStorage:
    """Guarda en archivo."""

    def save(self, data: dict, filename: str) -> None:
        print(f" Guardado en archivo: {filename}")


class CloudStorage:
    """Guarda en la nube."""

    def save(self, data: dict, filename: str) -> None:
        print(f" Guardado en nube: {filename}")


class DatabaseStorage:
    """Guarda en base de datos."""

    def save(self, data: dict, filename: str) -> None:
        print(f" Guardado en DB: {filename}")


# Protocol para la interfaz
class Storage(Protocol):
    """Cualquier cosa que pueda guardar datos."""

    def save(self, data: dict, filename: str) -> None: ...


# Tu aplicación acepta CUALQUIER tipo de storage
def backup_user_data(storage: Storage, user_data: dict) -> None:
    """Hace backup sin importar dónde se guarde."""
    print(f"Haciendo backup de {len(user_data)} campos...")
    storage.save(user_data, "user_backup")


# Funciona con todos, sin modificar backup_user_data
print("\n--- Sistema de Backup Flexible ---")
backup_user_data(FileStorage(), {"name": "Ana", "email": "ana@ex.com"})
backup_user_data(CloudStorage(), {"name": "Luis", "email": "luis@ex.com"})
backup_user_data(DatabaseStorage(), {"name": "Marta", "email": "marta@ex.com"})

# %% [markdown]
# ### Protocol vs Herencia: Cuándo Usar Cada Uno
#
# | Aspecto | Herencia (`ABC`) | Protocol |
# |---------|------------------|----------|
# | Necesita `class Foo(Base)` | Sí, obligatorio | No, automático |
# | Relación "es un" | Sí | No necesaria |
# | Flexibilidad | Limitada (árbol fijo) | Alta (cualquier clase funciona) |
# | Type hints mejores | Sí | Sí, además sin acoplamiento |
# | Mejor para datos reales | No | Sí |

# %% [markdown]
# ### Resumen: Protocol
#
# **Protocol** es "duck typing con seguridad de tipos":
# - Si cammina como un pato
# - Y suena como un pato
# - Python lo trata como un pato
#
# **Ventajas:**
# -  Sin herencia incómoda
# -  Flexible - cualquier clase funciona
# -  Type hints sin acoplamiento
# -  Mejor para datos reales que varían
#
# **Cuándo usar:**
# - Tienes múltiples clases con métodos similares
# - No quieres dependencias de herencia
# - Quieres type hints pero flexibilidad

# %% [markdown]
# ## Resumen
#
# - No todas las validaciones deben retornar `False`.
# - Una excepción específica hace más claro el error operacional.
# - **Excepciones con contexto:** incluye campo, valor, razón, número de fila.
# - **Elige el tipo correcto:** ValueError, TypeError, custom, o RuntimeError.
# - **Protocol:** interfaz sin herencia para casos avanzados.
