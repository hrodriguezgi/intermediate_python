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
# ## Resumen
#
# - Usa `list` cuando el orden y la edición importan.
# - Usa `tuple` para grupos pequeños y estables.
# - Usa `dict` para datos etiquetados.
# - Usa `set` para unicidad y pertenencia.
# - Usa `deque` para colas y una `list` para stacks sencillos.
