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
comprehension_result = [x * x for x in range(10)]
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
sample_csv.write_text("id,name,value\n1,Alice,100\n2,Bob,200\n3,Charlie,300\n")


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
# ## Escenario real: Crear procesadores de datos reutilizables
#
# **Problema en ETL:** Procesas datos de diferentes fuentes con reglas diferentes.
# Sin higher-order functions: repites código para cada fuente.
# Con higher-order functions: creas procesadores configurables.


# %%
def create_data_processor(transformation_rules: dict):
    """
    Crea un procesador de datos personalizado.

    Cada procesador aplica transformaciones específicas a campos.
    Reutilizable para múltiples registros/lotes.
    """

    def process(record: dict) -> dict:
        """Aplica transformaciones a un registro."""
        result = record.copy()
        for field, transform in transformation_rules.items():
            if field in result and result[field] is not None:
                try:
                    result[field] = transform(result[field])
                except Exception as e:
                    raise ValueError(f"Error transformando {field}: {e}")
        return result

    return process


# %%

# Caso 1: Procesar datos de usuarios
# Nota: lambda permite combinar múltiples transformaciones
user_processor = create_data_processor(
    {
        "email": lambda x: str.strip(x).lower(),  # Limpiar y minúsculas
        "name": str.strip,  # Quitar espacios en blanco
        "age": int,  # Convertir a entero
    }
)

# Caso 2: Procesar datos de transacciones
transaction_processor = create_data_processor(
    {
        "amount": float,  # Convertir a número
        "reference": lambda x: str.strip(x).upper(),  # Limpiar y mayúsculas
        "date": str.strip,  # Limpiar espacios
    }
)

# %%
# Uso: diferentes fuentes, mismo patrón

user_raw = {"email": "  USER@EXAMPLE.COM  ", "name": "  alice  ", "age": "30"}
user_cleaned = user_processor(user_raw)
print(f"Usuario limpiado: {user_cleaned}")

transaction_raw = {"amount": "  150.50  ", "reference": "  txn_001  ", "date": "2025-07-16"}
transaction_cleaned = transaction_processor(transaction_raw)
print(f"Transacción limpiada: {transaction_cleaned}")

# %% [markdown]
# ## Ventaja: Crear especializadas sin repetir código
#
# Cada procesador está configurado una vez,
# se reutiliza miles de veces en lotes.


# %%
# Procesar lotes completos
users_raw = [
    {"email": "ALICE@EXAMPLE.COM", "name": "alice smith", "age": "30"},
    {"email": "BOB@EXAMPLE.COM", "name": "bob jones", "age": "25"},
    {"email": "CHARLIE@EXAMPLE.COM", "name": "charlie brown", "age": "35"},
]

users_cleaned = [user_processor(user) for user in users_raw]

print("Lote de usuarios limpiados:")
for user in users_cleaned:
    print(f"  - {user['name']} ({user['email']}), edad: {user['age']}")

# %% [markdown]
# ## Resumen: funciones de orden superior
#
# - **apply_pipeline:** Encadena operaciones (una tras otra)
# - **create_data_processor:** Crea procesadores especializados (configurables)
# - Ambas son reutilizables y evitan repetir código

# %% [markdown]
# ## Decoradores: Modificar comportamiento sin cambiar código
#
# Un decorador envuelve una función añadiendo funcionalidad:
# logging, timing, validación, caché, etc.
#
# **Patrón:** función_original -> decorador -> función_mejorada


# %%
# Ejemplo básico: @traced
def traced(function):
    """Decorador que imprime entrada y salida de función."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"calling {function.__name__} with args={args}, kwargs={kwargs}")
        result = function(*args, **kwargs)
        print(f"returned {result}")
        return result

    return wrapper


@traced
def compute_discount(total: float, rate: float) -> float:
    """Calcula descuento (usado con @traced para ver qué pasa)."""
    return round(total * (1 - rate), 2)


total = compute_discount(250, 0.15)
print(total)

# %% [markdown]
# ## Cuándo usar decoradores
#
# **Casos de uso reales:**
#
# - **Logging:** Saber qué funciones se ejecutan, con qué argumentos
# - **Timing:** Medir cuánto tarda cada paso (crítico en ETL)
# - **Validación:** Verificar argumentos antes de ejecutar
# - **Caché:** Guardar resultados para evitar recálculos
# - **Reintento:** Reintentar si falla (para APIs inestables)
# - **Monitoreo:** Reportar errores o métricas a sistemas de alertas
#
# Los decoradores son perfectos para pipelines de datos donde necesitas
# visibilidad de qué está pasando sin modificar la lógica core.

# %% [markdown]
# ## Decoradores prácticos: @timing
#
# **Uso:** Mide cuánto tarda cada operación.
#
# **Por qué importa:**
# - ETL pipelines tienen cuellos de botella (¿dónde se demora?)
# - Detectar operaciones lentas sin agregar código en cada función
# - Monitorear performance en producción


# %%
import time


def timing(function):
    """Mide y reporta tiempo de ejecución."""

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
    """Simula lectura de datos (I/O lento)."""
    time.sleep(0.1)  # Simular I/O (disco, red)
    return [{"id": i, "value": i * 10} for i in range(100)]


@timing
def transform_data(records: list[dict]) -> list[dict]:
    """Simula transformación de datos."""
    time.sleep(0.05)  # Simular CPU
    return [{**record, "value": record["value"] * 2} for record in records]


data = load_data("data.csv")
transformed = transform_data(data)

# %% [markdown]
# Salida: Ves exactamente cuánto tarda cada paso sin modificar las funciones.

# %% [markdown]
# ## Decoradores prácticos: @log_calls
#
# **Uso:** Registra argumentos y resultado de cada llamada.
#
# **Por qué importa:**
# - Debugging: ¿Qué datos entra a la función?
# - Auditoría: Registrar qué validaciones fallaron y por qué
# - Testing: Verificar que se llama con argumentos correctos


# %%
def log_calls(function):
    """Registra argumentos de entrada y resultado de salida."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        args_str = ", ".join(repr(a) for a in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        print(f"{function.__name__}({all_args})")
        result = function(*args, **kwargs)
        print(f"  -> {result!r}")
        return result

    return wrapper


@log_calls
def validate_record(record: dict, strict: bool = False) -> bool:
    """Valida que un registro tenga campos requeridos."""
    if strict:
        required = ["id", "name", "email"]
        return all(key in record for key in required)
    return "id" in record


validate_record({"id": 1, "name": "Alice"})
validate_record({"id": 2, "name": "Bob", "email": "bob@example.com"}, strict=True)

# %% [markdown]
# Verás exactamente qué entra y qué sale, sin escribir print() en el código.

# %% [markdown]
# ## Escenario real: @monitoring para ETL
#
# Combina timing + logging + manejo de errores.
#
# **Objetivo:** Visibilidad completa de qué pasa en cada paso del pipeline:
# -  Cuánto tardó
# -  Cuántos registros procesó
# -  Si falló, cuándo y por qué


# %%
def monitoring(function):
    """Decora con timing, logging de éxito/fallo, y conteo de items."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = function(*args, **kwargs)
            elapsed = time.perf_counter() - start
            item_count = len(result) if isinstance(result, (list, dict)) else "?"
            print(f" {function.__name__} completado en {elapsed:.4f}s ({item_count} items)")
            return result
        except Exception as e:
            elapsed = time.perf_counter() - start
            print(f" {function.__name__} falló en {elapsed:.4f}s: {e}")
            raise

    return wrapper


@monitoring
def extract_from_source(source: str) -> list[dict]:
    """Extrae datos de una fuente (BD, API, archivo)."""
    return [{"id": i, "data": f"record_{i}"} for i in range(50)]


@monitoring
def validate_batch(records: list[dict]) -> list[dict]:
    """Valida lote de registros."""
    valid = [r for r in records if "id" in r and "data" in r]
    return valid


extracted = extract_from_source("database.db")
validated = validate_batch(extracted)

# %% [markdown]
# Output muestra cada paso: qué pasó, cuánto tardó, cuántos registros.

# %% [markdown]
# ## Funciones parciales para tuberías
#
# `functools.partial` prepara una función con argumentos fijos.
# Útil para configurar transformaciones reutilizables.


# %%
from functools import partial, reduce


# Función flexible que normaliza scores
def normalize_score(score: int | float, max_score: int) -> float:
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
