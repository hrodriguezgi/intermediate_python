# %% [markdown]
# # 02. Strings, colecciones y fechas
#
# ## Objetivos
#
# - Formatear texto de forma consistente.
# - Elegir entre `list`, `set`, `dict` y `tuple` con criterio.
# - Manipular fechas comunes en automatizaciones y reportes.

# %%
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta

release_name = "python intermediate revamp"
print(release_name.title())
print(release_name.upper())

# %% [markdown]
# ## F-strings
#
# Son la forma más clara para interpolar valores y controlar formatos de salida.

# %%
completion_rate = 0.8734
students = 28

summary = f"Completion rate: {completion_rate:.1%} | Students: {students}"
print(summary)

# %% [markdown]
# ## `split`, `join` y normalización básica

# %%
raw_tags = "python,files,sqlite,functions,python"
tags = [tag.strip() for tag in raw_tags.split(",")]

print(tags)
print(" | ".join(sorted(set(tags))))

# %% [markdown]
# ## Contar elementos
#
# `Counter` sirve para frecuencias y `defaultdict` evita condicionales repetidos
# cuando agrupas información.

# %%
topic_counter = Counter(tags)
print(topic_counter)

students_by_track = defaultdict(list)
students_by_track["backend"].extend(["Ana", "Luis"])
students_by_track["data"].append("Marta")

print(dict(students_by_track))

# %% [markdown]
# ## Fechas
#
# Las clases `date` y `datetime` son suficientes para una gran parte del trabajo
# de automatización diaria.

# %%
today = date.today()
next_week = today + timedelta(days=7)
print("today:", today.isoformat())
print("next_week:", next_week.isoformat())

# %%
published_at = datetime.fromisoformat("2026-06-22T09:30:00")
print(published_at.strftime("%d/%m/%Y %H:%M"))

# %% [markdown]
# ## Ordenar estructuras complejas

# %%
lessons = [
    {"name": "Funciones", "minutes": 60},
    {"name": "Archivos", "minutes": 45},
    {"name": "SQLite", "minutes": 75},
]

sorted_lessons = sorted(lessons, key=lambda lesson: lesson["minutes"], reverse=True)
print(sorted_lessons)

# %% [markdown]
# ## Resumen
#
# - `f-strings` son el formato por defecto.
# - `Counter` y `defaultdict` resuelven patrones muy comunes.
# - `datetime` cubre la mayoría de necesidades operativas.
