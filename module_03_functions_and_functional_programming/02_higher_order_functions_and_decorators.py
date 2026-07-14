# %% [markdown]
# # 02. Higher-order functions y decoradores
#
# ## Objetivos
#
# - Pasar funciones como argumentos.
# - Reutilizar comportamientos transversales.

# %%
from functools import wraps

numbers = [5, 12, 18, 21]

# %% [markdown]
# ## Expresiones generadoras vs comprensiones de lista
#
# **El problema:** Las comprensiones cargan TODO en memoria.
# Con millones de registros, esto crash o consume GB de RAM.


# %%
import timeit

# Comprensión de lista: carga todo en memoria
comprehension_result = [x * x for x in range(100000)]
print(f"Comprensión: {len(comprehension_result)} valores en memoria")

# Expresión generadora: evaluación perezosa
generator_result = (x * x for x in range(100000))
print(f"Generador: no consume memoria hasta iterar")

# %% [markdown]
# ## Impacto de memoria: el escenario real
#
# Procesar un CSV de 100GB línea por línea sin cargar todo.


# %%
import csv
from pathlib import Path

sample_csv = Path("/tmp/sample_data.csv")

# Crear archivo de ejemplo
sample_csv.write_text(
    "id,name,value\n1,Alice,100\n2,Bob,200\n3,Charlie,300\n"
)

# MAL: cargar todo en memoria (crash con archivos grandes)
def load_all_wrong(path):
    with open(path) as f:
        rows = [dict(row) for row in csv.DictReader(f)]
    return rows


# BIEN: iterar línea por línea con generador
def load_streaming(path):
    with open(path) as f:
        for row in csv.DictReader(f):
            yield row


# Uso: procesar un registro a la vez
for record in load_streaming(sample_csv):
    print(f"Procesando: {record['id']} - {record['name']}")

# %% [markdown]
# ## Cuándo usar cada una
#
# - **Comprensión de lista**: datos pequeños, necesitas la lista completa
# - **Expresión generadora**: datos grandes, procesas secuencialmente

# %%
# `map` y `filter` (menos común en Python moderno)
squared = list(map(lambda value: value * value, numbers))
large_values = list(filter(lambda value: value >= 15, numbers))

print(squared)
print(large_values)

# %% [markdown]
# ## Funciones de orden superior


# %%
def apply_pipeline(values: list[int], *operations) -> list[int]:
    result = values
    for operation in operations:
        result = operation(result)
    return result


def keep_even(values: list[int]) -> list[int]:
    return [value for value in values if value % 2 == 0]


def double(values: list[int]) -> list[int]:
    return [value * 2 for value in values]


print(apply_pipeline(numbers, keep_even, double))

# %% [markdown]
# ## Decoradores


# %%
def traced(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"calling {function.__name__} with args={args}, kwargs={kwargs}")
        result = function(*args, **kwargs)
        print(f"returned {result}")
        return result

    return wrapper


@traced
def compute_discount(total: float, rate: float) -> float:
    return round(total * (1 - rate), 2)


compute_discount(250, 0.15)

# %% [markdown]
# ## Decoradores prácticos: @timing
#
# En pipelines ETL, necesitas medir cuánto tiempo toma cada operación.


# %%
import time

def timing(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{function.__name__} tardó {elapsed:.4f}s")
        return result

    return wrapper


@timing
def load_data(path: str) -> list[dict]:
    time.sleep(0.1)  # Simular I/O
    return [{"id": i, "value": i * 10} for i in range(100)]


@timing
def transform_data(records: list[dict]) -> list[dict]:
    time.sleep(0.05)  # Simular procesamiento
    return [
        {**record, "value": record["value"] * 2}
        for record in records
    ]


data = load_data("data.csv")
transformed = transform_data(data)

# %% [markdown]
# ## Decoradores prácticos: @log_calls
#
# Ver qué argumentos se pasan a una función (útil para debugging).


# %%
def log_calls(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        print(f"{function.__name__}({all_args})")
        result = function(*args, **kwargs)
        print(f"  → {result!r}")
        return result

    return wrapper


@log_calls
def validate_record(record: dict, strict: bool = False) -> bool:
    if strict:
        required = ["id", "name", "email"]
        return all(key in record for key in required)
    return "id" in record


validate_record({"id": 1, "name": "Alice"})
validate_record({"id": 2, "name": "Bob", "email": "bob@example.com"}, strict=True)

# %% [markdown]
# ## Escenario real: monitoreo de ETL
#
# Combina timing + logging para rastrear qué tarda en un pipeline.


# %%
def monitoring(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = function(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(
                f"✓ {function.__name__} completado en {elapsed:.4f}s "
                f"({len(result) if isinstance(result, (list, dict)) else '?'} items)"
            )
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start
            print(f"✗ {function.__name__} falló en {elapsed:.4f}s: {e}")
            raise

    return wrapper


@monitoring
def extract_from_source(source: str) -> list[dict]:
    return [{"id": i, "data": f"record_{i}"} for i in range(50)]


@monitoring
def validate_batch(records: list[dict]) -> list[dict]:
    valid = [r for r in records if "id" in r and "data" in r]
    return valid


extracted = extract_from_source("database.db")
validated = validate_batch(extracted)

# %% [markdown]
# ## Funciones parciales para tuberías
#
# `functools.partial` prepara una función con argumentos fijos.
# Útil para configurar transformaciones reutilizables.


# %%
from functools import partial
from functools import reduce

# Función flexible que normaliza scores
def normalize_score(score: int | float, max_score: int = 100) -> float:
    return round(score / max_score, 2)


# Sin partial: necesitas wrappers
def normalize_to_100(score):
    return normalize_score(score, max_score=100)


def normalize_to_200(score):
    return normalize_score(score, max_score=200)


# Con partial: elegante
normalize_100 = partial(normalize_score, max_score=100)
normalize_200 = partial(normalize_score, max_score=200)

print(f"Score 85 en escala 100: {normalize_100(85)}")
print(f"Score 150 en escala 200: {normalize_200(150)}")

# %% [markdown]
# ## Escenario real: tuberías de transformación CSV
#
# Prepara transformaciones y cómbinalas en una tubería.


# %%
# Función base flexible
def clean_data(value: str, steps: list) -> str:
    """Aplica pasos de limpieza secuencialmente."""
    for step in steps:
        value = step(value)
    return value


# Define transformaciones reutilizables
strip_ws = str.strip
to_upper = str.upper
add_suffix = partial(lambda x, suffix: f"{x}{suffix}", suffix="_processed")

# Crea pipelines para diferentes campos
clean_id_pipeline = partial(clean_data, steps=[strip_ws, to_upper])
clean_name_pipeline = partial(clean_data, steps=[strip_ws, to_upper])

# Registro sin procesar
record = {"id": "  a123  ", "name": "  alice smith  "}

# Aplica transformaciones
record["id"] = clean_id_pipeline(record["id"])
record["name"] = clean_name_pipeline(record["name"])

print(f"Record procesado: {record}")

# %% [markdown]
# ## Ventaja: reutilizar y componer
#
# Define transformaciones una vez, úsalas en múltiples lugares.


# %%
# Transformaciones reutilizables
normalize_100_partial = partial(normalize_score, max_score=100)
normalize_200_partial = partial(normalize_score, max_score=200)

scores_100 = [88, 91, 74]
scores_200 = [150, 180, 140]

# Aplicar a diferentes escalas
normalized_100 = [normalize_100_partial(s) for s in scores_100]
normalized_200 = [normalize_200_partial(s) for s in scores_200]

print(f"Scores (escala 100): {normalized_100}")
print(f"Scores (escala 200): {normalized_200}")

# %% [markdown]
# ## Resumen
#
# - Una función puede ser un dato más dentro del programa.
# - Los decoradores permiten encapsular trazabilidad y validación.
# - `@timing` mide rendimiento de operaciones.
# - `@log_calls` registra entradas y salidas para debugging.
# - `functools.partial` configura funciones reutilizables para pipelines.
