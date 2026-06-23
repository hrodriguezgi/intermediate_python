# %% [markdown]
# # 01. Tipos de datos y variables
#
# ## Objetivos
#
# - Repasar los tipos básicos que aparecen en casi cualquier script.
# - Entender cómo cambian los valores al convertir entre tipos.
# - Recordar cómo Python evalúa condiciones con truthy y falsy.

# %%
course_name = "Intermediate Python"
module_number = 0
duration_hours = 2.5
is_intro_module = True

print(type(course_name).__name__)
print(type(module_number).__name__)
print(type(duration_hours).__name__)
print(type(is_intro_module).__name__)

# %% [markdown]
# ## Tipos numéricos
#
# `int` y `float` cubren la mayoría de cálculos cotidianos en scripts,
# automatizaciones y validaciones simples.

# %%
registered_students = 24
average_score = 4.7

print(registered_students + 6)
print(round(average_score * 10, 1))

# %% [markdown]
# ## Booleanos
#
# `bool` representa verdadero o falso. Suele aparecer en validaciones, banderas
# de configuración y resultados de comparaciones.

# %%
is_open = True
has_pending_homework = False

print(is_open and not has_pending_homework)

# %% [markdown]
# ## Strings
#
# Los strings modelan nombres, mensajes, rutas, etiquetas y prácticamente
# cualquier dato textual.

# %%
student_name = "  ana maria  "

print(student_name.strip().title())
print(f"Welcome, {student_name.strip().title()}!")

# %% [markdown]
# ## Variables y reasignación
#
# Una variable es un nombre que apunta a un objeto. El nombre puede reutilizarse
# para referenciar otro valor más adelante.

# %%
topic = "data types"
print(topic)

topic = "data structures"
print(topic)

# %% [markdown]
# ## Conversión entre tipos
#
# Convertir tipos es parte del trabajo diario cuando lees archivos, parámetros o
# datos de entrada de usuarios.

# %%
raw_students = "24"
raw_completion_rate = "0.82"

students = int(raw_students)
completion_rate = float(raw_completion_rate)
summary = f"Students: {students} | Completion: {completion_rate:.0%}"

print(summary)

# %% [markdown]
# ## Operaciones básicas
#
# Python mantiene una sintaxis directa para aritmética y comparaciones.

# %%
completed_lessons = 3
total_lessons = 8
pending_lessons = total_lessons - completed_lessons

print("pending_lessons:", pending_lessons)
print("module_ready:", completed_lessons >= 2)
print("same_total:", total_lessons == 8)

# %% [markdown]
# ## Truthy y falsy
#
# Valores vacíos o cero suelen evaluarse como `False`, mientras que valores con
# contenido suelen evaluarse como `True`.

# %%
examples = [
    ("empty string", ""),
    ("zero", 0),
    ("empty list", []),
    ("course name", "Python"),
    ("student count", 12),
]

for label, value in examples:
    print(f"{label:<12} -> {bool(value)}")

# %% [markdown]
# ## `None` vs Empty Containers (Gotcha importante)
#
# Un error común es confundir `None` con contenedores vacíos como `[]` o `{}`.
# Ambos son "falsy", pero tienen significados muy diferentes en la lógica de datos.
#
# En pipelines reales:
# - `None` típicamente significa "no fue asignado" o "no existe"
# - `[]` significa "existe, pero no tiene elementos"
# - Esta diferencia importa para validación y configuración

# %%
def process_data(values):
    """El problema: if values captura tanto [] como None"""
    if values:
        return sum(values)
    return 0  # ¿Es 0 lo correcto para [] Y None?

# Sin distinguir, pierdes información valiosa:
print("Empty list result:", process_data([]))      # Retorna 0
print("None result:", process_data(None))          # También retorna 0
print("¿Cómo diferencias si fue None o []?")

# %% [markdown]
# La solución: verifica explícitamente con `is None`

# %%
def process_data_correct(values):
    """Distingue entre None y contenedor vacío"""
    if values is None:
        raise ValueError("values is required, got None")
    if not values:
        return 0  # Ahora sabemos que es []
    return sum(values)

# Ahora puedes manejar cada caso:
print("Empty list with check:", process_data_correct([]))
try:
    process_data_correct(None)
except ValueError as e:
    print(f"Caught error: {e}")

# %% [markdown]
# Escenario real en pipelines de datos:
# Configuración donde `None` = "usar default" y `[]` = "deshabilitado"

# %%
def configure_tags(user_tags=None, default_tags=None):
    """
    None = usar defaults
    [] = deshabilitado explícitamente
    ["tag1", "tag2"] = usar estos
    """
    if user_tags is None:
        # None significa "no fue configurado", usar defaults
        tags = default_tags or ["python"]
    elif len(user_tags) == 0:
        # [] significa "deshabilitado explícitamente"
        tags = []
    else:
        # Se especificaron etiquetas
        tags = user_tags

    return tags

print("No config (None):", configure_tags())
print("Explicit empty []:", configure_tags(user_tags=[]))
print("Specific tags:", configure_tags(user_tags=["advanced", "data"]))

# %% [markdown]
# ## `None`
#
# `None` representa la ausencia intencional de un valor y aparece con frecuencia
# en funciones, configuración y flujos condicionales.

# %%
next_module = None

if next_module is None:
    print("Next module has not been assigned yet.")

# %% [markdown]
# ## Resumen
#
# - Python trabaja con tipos básicos como `int`, `float`, `bool` y `str`.
# - Convertir tipos explícitamente evita errores silenciosos.
# - Truthy y falsy ayudan a escribir condiciones simples y legibles.
# - `None` comunica ausencia de valor de forma explícita.

# %%
