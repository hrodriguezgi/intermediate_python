# %% [markdown]
# # 02. Estructuras de datos básicas
#
# ## Objetivos
#
# - Diferenciar cuándo usar `list`, `tuple`, `dict` y `set`.
# - Practicar acceso, actualización y recorrido de estructuras comunes.
# - Introducir estructuras lineales simples como stack y queue.
# - Reforzar operaciones básicas que luego aparecen en el resto del curso.

# %%
from collections import deque

topics = ["variables", "types", "lists", "dicts"]
checkpoints = ("syntax", "conditions", "loops")
student = {"name": "Ana", "track": "backend", "active": True}
unique_tracks = {"backend", "data", "backend"}

print(topics)
print(checkpoints)
print(student)
print(unique_tracks)

# %% [markdown]
# ## Listas
#
# Son útiles cuando importa el orden y necesitas agregar, quitar o transformar
# elementos.

# %%
topics.append("files")
first_two_topics = topics[:2]

print("updated topics:", topics)
print("first two:", first_two_topics)

# %% [markdown]
# ## Tuplas
#
# Son una buena opción para agrupar datos fijos que no deberían cambiar durante
# el flujo normal del programa.

# %%
name, track, is_active = ("Luis", "data", True)
print(name, track, is_active)

# %% [markdown]
# ## Diccionarios
#
# Los diccionarios modelan información con nombre: configuraciones, registros,
# respuestas de APIs y muchas otras estructuras reales.

# %%
student["completed_lessons"] = 4
student["track"] = "platform"

print(student["name"])
print(student)

# %% [markdown]
# ## Conjuntos
#
# Los `set` eliminan duplicados y permiten revisar pertenencia rápidamente.

# %%
raw_tags = ["python", "basics", "python", "course", "basics"]
unique_tags = set(raw_tags)

print(sorted(unique_tags))
print("sqlite" in unique_tags)

# %% [markdown]
# ## Queue con `deque`
#
# Cuando necesitas procesar elementos en orden de llegada, una cola es una
# estructura natural. En Python, `collections.deque` es una opción práctica.

# %%
support_queue = deque(["ticket-101", "ticket-102", "ticket-103"])
support_queue.append("ticket-104")
next_ticket = support_queue.popleft()

print("next ticket:", next_ticket)
print("remaining queue:", list(support_queue))

# %% [markdown]
# ## Stack simple
#
# Un stack procesa el último elemento agregado primero. Una lista suele ser
# suficiente para este patrón básico.

# %%
undo_stack = ["draft-1", "draft-2"]
undo_stack.append("draft-3")
last_version = undo_stack.pop()

print("restored from stack:", last_version)
print("remaining versions:", undo_stack)

# %% [markdown]
# ## Elegir la estructura correcta: Performance importa
#
# En pipelines reales con millones de registros, la elección de estructura
# afecta drásticamente el rendimiento. Aquí mostramos qué pasa cuando eliges mal.

# %%
import timeit

# Escenario: Verificar si un ID existe en una colección (1 millón de IDs)
ids_list = list(range(1_000_000))
ids_set = set(range(1_000_000))

# Búsqueda en lista: O(n) - se vuelve lento rápido
time_list = timeit.timeit(
    lambda: 500_000 in ids_list,
    number=1000,
)

# Búsqueda en set: O(1) - constante, sin importar el tamaño
time_set = timeit.timeit(
    lambda: 500_000 in ids_set,
    number=1000,
)

print(f"List membership check (1M items): {time_list:.4f}s")
print(f"Set membership check (1M items): {time_set:.4f}s")
print(f"Set es ~{time_list/time_set:.0f}x más rápido")

# %% [markdown]
# Guía práctica para elegir:
#
# - **`list`**: Cuando necesitas orden y modificación (append, insert, pop)
# - **`tuple`**: Datos inmutables que irán en diccionarios o sets
# - **`dict`**: Acceso por clave (más rápido que buscar en lista)
# - **`set`**: Deduplicación y membresía (mucho más rápido que list)

# %%
# Ejemplo real: Pipeline ETL deduplicando IDs de usuarios

# LENTO: usando lista
processed_ids_slow = []
for user_id in range(100_000):
    if user_id not in processed_ids_slow:  # O(n) cada vez!
        processed_ids_slow.append(user_id)

# RÁPIDO: usando set
processed_ids_fast = set()
for user_id in range(100_000):
    if user_id not in processed_ids_fast:  # O(1) siempre
        processed_ids_fast.add(user_id)

print(f"\nDeduplication comparison:")
print(f"List approach: {len(processed_ids_slow)} unique")
print(f"Set approach: {len(processed_ids_fast)} unique")

# %% [markdown]
# ## Recorrer estructuras
#
# Combinar `for`, `enumerate` y `.items()` cubre una gran parte del trabajo
# cotidiano con colecciones.

# %%
for index, topic in enumerate(topics, start=1):
    print(f"{index}. {topic}")

for key, value in student.items():
    print(f"{key}: {value}")

# %% [markdown]
# ## Los datos reales son desordenados
#
# APIs, CSVs y logs rara vez tienen tipos "puros". Prepararse para datos
# mixtos es crítico en cualquier pipeline.

# %%
# Escenario real: Respuesta JSON de API con problemas de tipo

api_response = {
    "id": 1,
    "name": "Alice",
    "age": "30",  # ¡String, no int!
    "score": None,  # Ausente
    "tags": "python,data",  # String, no lista
    "active": "yes",  # String, no bool
}

# PROBLEMA: Asumir tipos causa errores

# %%
# Manejo defensivo de tipos mixtos

def safe_get_int(value, default=0):
    """Convierte a int de forma segura"""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_get_bool(value, default=False):
    """Convierte a bool de forma segura"""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("yes", "true", "1", "on")
    return bool(value)

# Procesa los datos con seguridad
age = safe_get_int(api_response["age"])
is_active = safe_get_bool(api_response["active"])
score = safe_get_int(api_response["score"], default=0)
tags = api_response["tags"].split(",") if isinstance(api_response["tags"], str) else api_response["tags"]

print(f"Parsed safely:")
print(f"  age: {age} (type: {type(age).__name__})")
print(f"  active: {is_active} (type: {type(is_active).__name__})")
print(f"  score: {score} (type: {type(score).__name__})")
print(f"  tags: {tags}")

# %% [markdown]
# Caso de uso real: Lectura de CSV con tipos inconsistentes

# %%
import csv
from io import StringIO

# CSV con tipos inconsistentes (como ocurre en la vida real)
csv_data = """id,name,count,status
1,Alice,10,active
2,Bob,cinco,pending
3,Charlie,,active"""

reader = csv.DictReader(StringIO(csv_data))
records = []

for row in reader:
    # Valida y convierte tipos
    try:
        record = {
            "id": int(row["id"]),
            "name": row["name"].strip(),
            "count": safe_get_int(row["count"], default=0),
            "status": row["status"].lower(),
        }
        records.append(record)
    except Exception as e:
        print(f"Skipped row {row['id']}: {e}")

print("\nCSV records after cleanup:")
for record in records:
    print(record)

# %% [markdown]
# ## Resumen
#
# - Usa `list` cuando el orden y la edición importan.
# - Usa `tuple` para grupos pequeños y estables.
# - Usa `dict` para datos etiquetados.
# - Usa `set` para unicidad y pertenencia, **especialmente para búsquedas en datos grandes**.
# - Usa `deque` para colas y una `list` para stacks sencillos.
# - **Distigue explícitamente entre `None` y contenedores vacíos.**
# - **Los datos reales son desordenados: valida tipos defensivamente.**
