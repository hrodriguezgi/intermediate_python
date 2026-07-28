# %% [markdown]
# # 02. Excepciones y validación
#
# ## Objetivos
#
# - Fallar con mensajes útiles.
# - Crear excepciones específicas cuando aporta claridad.

# %%
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

    def __init__(
        self, field: str, value: object, reason: str, row_num: int | None = None
    ):
        self.field = field
        self.value = value
        self.reason = reason
        self.row_num = row_num

        location = f" (row {row_num})" if row_num else ""
        message = (
            f"Validation failed{location}: {field}={value!r} - {reason}"
        )
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
        print(f"Row {i}: ✓ Valid")
    except DataValidationError as e:
        print(f"Row {i}: ✗ {e}")
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
def process_with_callback(
    data: list, callback: Callable[[object], object] | None = None
) -> list:
    if callback is not None and not callable(callback):
        raise TypeError(
            f"callback must be callable, got {type(callback).__name__}"
        )
    return [callback(x) if callback else x for x in data]


# Excepciones personalizadas: violación de lógica de negocio
class InsufficientFundsError(Exception):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Insufficient funds: balance={balance}, requested={amount}"
        )


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
# ## Protocol Types (Avanzado)
#
# Para interfaces más limpias sin herencia, usa `Protocol`.

# %%


class DataLoader(Protocol):
    """Interfaz estructural: cualquier objeto con método load() funciona."""

    def load(self) -> dict:
        ...


class SimpleCSVLoader:
    def load(self) -> dict:
        return {"rows": 100}


class APILoader:
    def load(self) -> dict:
        return {"items": 50}


def process_data(loader: DataLoader) -> None:
    """Acepta cualquier objeto que tenga método load()."""
    data = loader.load()
    print(f"Procesando {len(data)} items")


# Ambas funcionan sin herencia explícita
process_data(SimpleCSVLoader())
process_data(APILoader())

# %% [markdown]
# Protocol es como "duck typing con type hints": si camina como DataLoader y
# suena como DataLoader, Python lo trata como DataLoader.

# %% [markdown]
# ## Resumen
#
# - No todas las validaciones deben retornar `False`.
# - Una excepción específica hace más claro el error operacional.
# - **Excepciones con contexto:** incluye campo, valor, razón, número de fila.
# - **Elige el tipo correcto:** ValueError, TypeError, custom, o RuntimeError.
# - **Protocol:** interfaz sin herencia para casos avanzados.
