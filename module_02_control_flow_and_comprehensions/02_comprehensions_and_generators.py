# %% [markdown]
# # 02. Comprehensions y generadores
#
# ## Objetivos
#
# - Usar comprehensions cuando la transformación es simple.
# - Entender generadores para procesar datos grandes sin cargar todo en memoria.
# - Conocer cuándo usar comprehensions vs generadores según el tamaño de datos.

# %%
events = [
    {"user": "ana", "duration": 35, "status": "ok"},
    {"user": "luis", "duration": 12, "status": "retry"},
    {"user": "marta", "duration": 48, "status": "ok"},
    {"user": "analu", "duration": 20, "status": "ok"},
]

# %% [markdown]
# ## List comprehensions

"""
succesful_durations = list()
for event in events:
    if event["status"] == "ok":
        successful_durations.append(event["duration"])
"""

# %%
successful_durations = (event["duration"] for event in events if event["status"] == "ok")
print(tuple(successful_durations))

# %% [markdown]
# ## Dict comprehensions

# %%
latest_duration_by_user = {event["user"]: (event["duration"], event["status"]) for event in events if event["status"] == "ok"}
print(latest_duration_by_user)
# %%
"""
latest_duration_by_user = dict()
for event in events:
    user = event['user']
    duration = event['duration']
    latest_duration_by_user[user] = duration

"""

# %% [markdown]
# ## Set comprehensions

# %%
active_users = {event["user"] for event in events if event["duration"] >= 20}
print(active_users)

# %% [markdown]
# ## Generadores (funciones con `yield`) -> lazy
#
# Son una buena opción para procesar secuencias largas sin cargar todo en memoria.

# %%
events = [
    {"user": "ana", "duration": 35, "status": "ok"},
    {"user": "luis", "duration": 12, "status": "retry"},
    {"user": "marta", "duration": 48, "status": "ok"},
    {"user": "analu", "duration": 20, "status": "ok"},
]

# %%
def durations_over(limit: int):
    for event in events:
        if event["duration"] > limit:
            yield event["duration"]


for duration in durations_over(20): 
    print(duration)

# %%
duration = durations_over(20)
# %%
print(next(duration, None))
# %%
def contador():
    yield 1
    yield 2
    yield 3

valor = contador()
print(valor)

# %%
print(next(valor, None))

# %% [markdown]
# ## Expresiones generador vs list comprehensions
#
# **El problema:** Con datos grandes, una list comprehension carga TODO en memoria.
# Una expresión generador procesa un elemento a la vez.
#
# En pipelines de datos reales (millones de filas), esto es crítico.


# %%
# Real scenario: Procesar un CSV muy grande (100M filas)

# List comprehension: carga TODO en memoria
# results = [transform(row) for row in huge_dataset]  # Needs GB of RAM

# with open("mi_archivo.csv", "r"): as f:
#     data = f.read()
# 
# 
# file = open("mi_archivo.csv", "r")
# data_2 = file.read()
# file.close()

def lazy_read_csv(filename: str):
    with open(filename) as f:
        for line in f.readlines():
            yield from line





# Expresión generador: procesa fila por fila
def process_large_dataset(rows):
    for row in rows:
        if row.get("status") == "ok":
            yield row["duration"] * 2


# Simulating a lazy iteration
fake_dataset = iter(events)
results = (event["duration"] * 2 for event in fake_dataset if event["status"] == "ok")

# Consumir bajo demanda (una a la vez)
print("Generator expression (lazy):")
for result in results:
    print(f"  Processed: {result}")

# %% [markdown]
# ## Cuándo usar cada una
#
# | Caso | Usa |
# |------|-----|
# | Datos pequeños (<1000 elementos) | List comprehension |
# | Necesitas reutilizar varias veces | List comprehension |
# | Datos grandes (millones) | Expresión generador |
# | Procesamiento en streaming | Generador con `yield` |
# | Solo necesitas iterar una vez | Generador |


# %%
# Comparación
small_events = events  # Just for demo

# Comprehension: lista completa en memoria
list_result = [e["duration"] for e in small_events if e["status"] == "ok"]
print(f"List comprehension result: {list_result}")

# Generator expression: evaluado bajo demanda
gen_result = (e["duration"] for e in small_events if e["status"] == "ok")
print(f"Generator expression result: {gen_result}")  # Solo muestra el objeto generador

# Consumir el generador
print("Consuming generator:")
for item in gen_result:
    print(f"  {item}")

# %% [markdown]
# ## Resumen
#
# - Las comprehensions funcionan bien para una transformación puntual con datos pequeños.
# - Los generadores (funciones con `yield` o expresiones) escalan para datos grandes.
# - En pipelines de datos, usa generadores para evitar sobrecargar memoria.
