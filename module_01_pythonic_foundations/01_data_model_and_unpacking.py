# %% [markdown]
# # 01. Modelo de datos y desempaque
#
# ## Objetivos
#
# - Revisar cómo Python referencia objetos en memoria.
# - Diferenciar estructuras mutables e inmutables.
# - Usar asignación múltiple y desempaque para escribir código más expresivo.
#
# ## Idea clave
#
# En Python una variable no almacena el valor en sí mismo, sino una referencia
# a un objeto. Esa decisión explica por qué algunas operaciones mutan un objeto
# existente y otras crean uno nuevo.

# %%
from pprint import pprint

course = "Intermediate Python"
students = ["Ana", "Luis", "Marta"]
metadata = {"level": "intermediate", "duration_weeks": 6}

print(course)
print(students)
print(metadata)

# %% [markdown]
# ## Mutabilidad
#
# Las tuplas, cadenas y enteros son inmutables. Las listas y diccionarios sí
# pueden cambiar después de creados.

# %%
schedule = ["variables", "collections", "functions"]
alias = schedule

schedule.append("files")

print("schedule:", schedule)
print("alias:", alias)
print("same object:", schedule is alias)

# %% [markdown]
# ## Copias superficiales
#
# Cuando quieres cambiar una lista sin afectar la referencia original, crea una
# nueva lista con `list(...)` o con slicing.

# %%
safe_schedule = list(schedule)
safe_schedule.remove("collections")

print("original:", schedule)
print("copy:", safe_schedule)

# %% [markdown]
# ## Asignación múltiple y desempaque
#
# Estas operaciones mejoran la legibilidad cuando los datos ya tienen una
# estructura conocida.

# %%
first_topic, second_topic, *remaining_topics = schedule

print(first_topic)
print(second_topic)
print(remaining_topics)

# %%
teacher = ("Helena", "Backend", 7)
name, specialty, years_experience = teacher

print(name, specialty, years_experience)

# %% [markdown]
# ## `enumerate` y `zip`
#
# Son dos herramientas simples pero muy útiles para recorrer datos paralelos sin
# administrar índices manualmente.

# %%
durations = [30, 45, 60, 50]
paired = list(zip(schedule, durations, strict=True))

pprint(paired)

for lesson_number, (topic, minutes) in enumerate(paired, start=1):
    print(f"{lesson_number}. {topic:<12} -> {minutes} minutos")

# %% [markdown]
# ## Diccionarios con desempaque
#
# El operador `**` permite combinar configuraciones sin mutar el diccionario
# original.

# %%
default_config = {"theme": "dark", "language": "es", "autosave": False}
user_config = {"autosave": True, "font_size": 14}

final_config = {**default_config, **user_config}
print(final_config)

# %% [markdown]
# ## Resumen
#
# - Las variables referencian objetos.
# - La mutabilidad impacta cómo se comparten cambios.
# - El desempaque y `zip` reducen ruido accidental.
# - Combinar estructuras de forma explícita mejora el diseño del código.
