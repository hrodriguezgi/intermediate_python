# %% [markdown]
# # 01. Diseño de funciones
#
# ## Objetivos
#
# - Separar responsabilidades.
# - Definir funciones con entradas y salidas claras.
# - Reducir efectos secundarios.

# %%
from statistics import mean

scores = [88, 91, 74, 100, 95]

# %% [markdown]
# ## Funciones puras
#
# Una función pura depende sólo de sus argumentos y retorna un valor nuevo.


# %%
def normalize_score(score: int, max_score: int = 100) -> float:
    return round(score / max_score, 2)


normalized_scores = [normalize_score(score) for score in scores]
print(normalized_scores)

# %% [markdown]
# ## Funciones con nombre claro


# %%
def build_grade_report(raw_scores: list[int]) -> dict:
    return {
        "count": len(raw_scores),
        "average": round(mean(raw_scores), 2),
        "max": max(raw_scores),
        "min": min(raw_scores),
    }


print(build_grade_report(scores))

# %% [markdown]
# ## `*args` y `**kwargs`
#
# Úsalos cuando aportan flexibilidad real, no por costumbre.


# %%
def format_labels(*labels: str, uppercase: bool = False) -> list[str]:
    if uppercase:
        return [label.upper() for label in labels]
    return [label.title() for label in labels]


print(format_labels("python", "sqlite", uppercase=True))

# %% [markdown]
# ## Trampa: argumentos mutables por defecto
#
# Un error común: usar listas o diccionarios como valores por defecto.
# Se comparten entre todas las llamadas a la función.


# %%
# INCORRECTO: la lista se comparte
def collect_data_wrong(new_item, cache=[]):
    cache.append(new_item)
    return cache


result1 = collect_data_wrong("first")
print(f"First call: {result1}")

result2 = collect_data_wrong("second")
print(f"Second call: {result2}")  # ["first", "second"] - ¡comparten cache!

# %% [markdown]
# El problema: la lista `[]` se crea UNA SOLA VEZ cuando se define la función,
# no en cada llamada. Todas las llamadas reutilizan la misma lista.

# %%
# CORRECTO: crear el valor por defecto en cada llamada
def collect_data(new_item, cache=None):
    if cache is None:
        cache = []
    cache.append(new_item)
    return cache


result1 = collect_data("first")
print(f"First call: {result1}")

result2 = collect_data("second")
print(f"Second call: {result2}")  # ["second"] - listas independientes

# %% [markdown]
# ## Escenario real: tuberías de datos
#
# En pipelines ETL, esto causa bugs silenciosos donde múltiples registros
# comparten el mismo estado.


# %%
def process_record(record: dict, tags: list = None) -> dict:
    if tags is None:
        tags = []
    tags.append(record.get("id"))
    return {**record, "tags": tags}


# Cada registro debe tener sus propias tags
record1 = process_record({"id": 1, "name": "Alice"})
print(f"Record 1 tags: {record1['tags']}")

record2 = process_record({"id": 2, "name": "Bob"})
print(f"Record 2 tags: {record2['tags']}")  # Solo [2], no [1, 2]

# %% [markdown]
# ## Resumen
#
# - Una función pequeña es más fácil de validar.
# - Un nombre claro comunica la intención.
# - `*args` y `**kwargs` deben usarse con criterio.
# - Nunca uses mutables (`[]`, `{}`) como valores por defecto. Usa `None` en su lugar.
