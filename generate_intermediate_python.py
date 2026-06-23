from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COURSE_ROOT = ROOT / "intermediate_python"


FILES: dict[str, str] = {
    "README.md": """# Intermediate Python

Curso práctico de Python intermedio orientado a escribir código más expresivo, mantenible y útil para proyectos reales.

## Objetivos

- Consolidar bases sólidas de Python más allá de la sintaxis inicial.
- Practicar diseño de funciones, manejo de archivos, serialización, POO y SQLite.
- Tener una versión paralela de cada lección en script (`.py`) y notebook (`.ipynb`).
- Resolver ejercicios por módulo con formato `README.md`, `starter.py` y `solution.py`.

## Requisitos

- Python 3.12
- `uv` como package manager y runner del proyecto
- `ruff` y `flake8` como herramientas de formato y lint

## Estructura

```text
intermediate_python/
├── README.md
├── tools/
│   ├── build_notebooks.py
│   └── validate_course.py
├── module_01_pythonic_foundations/
├── module_02_control_flow_and_comprehensions/
├── module_03_functions_and_functional_programming/
├── module_04_files_serialization_and_paths/
├── module_05_oop_and_errors/
└── module_06_packages_and_sqlite/
```

## Flujo recomendado

1. Leer el `README.md` del módulo.
2. Ejecutar la lección con `uv run` usando el módulo Python.
3. Repasar el notebook equivalente en `notebooks/`.
4. Resolver el ejercicio correspondiente en `exercises/`.

## Setup

```bash
uv sync --group dev
```

## Utilidades

```bash
uv run python tools/build_notebooks.py
uv run python tools/validate_course.py
uv run python -m module_01_pythonic_foundations.01_data_model_and_unpacking
uv run python -m module_06_packages_and_sqlite.01_packages_imports_and_cli
uv run ruff check .
uv run ruff format .
uv run flake8 .
```

## Convenciones

- Usa `Python 3.12` para evitar incompatibilidades con `match` y otras features modernas.
- Prefiere imports absolutos dentro del paquete cuando una lección reutiliza código de otro archivo.
- Ejecuta scripts de módulos y ejercicios desde la raíz del repo con `uv run python -m ...`.
""",
    ".gitignore": """__pycache__/
.ipynb_checkpoints/
.DS_Store
""",
    ".python-version": """3.12
""",
    "pyproject.toml": """[project]
name = "intermediate-python-course"
version = "0.1.0"
description = "Hands-on intermediate Python course with matching scripts, notebooks, and exercises."
readme = "README.md"
requires-python = ">=3.12,<3.13"
dependencies = []

[dependency-groups]
dev = [
  "flake8>=7.1.0",
  "ruff>=0.6.9",
]

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "W", "B", "UP"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
""",
    "tools/build_notebooks.py": """from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_percent_script(script_path: Path) -> dict:
    lines = script_path.read_text(encoding="utf-8").splitlines()
    cells: list[tuple[str, list[str]]] = []
    current_type: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_type, current_lines
        if current_type is None:
            return
        while current_lines and current_lines[-1] == "":
            current_lines.pop()
        cells.append((current_type, current_lines[:]))
        current_type = None
        current_lines = []

    for line in lines:
        if line.startswith("# %%"):
            flush()
            current_type = "markdown" if "[markdown]" in line else "code"
            continue
        if current_type is None:
            current_type = "code"
        current_lines.append(line)

    flush()

    notebook_cells = []
    for cell_type, cell_lines in cells:
        if cell_type == "markdown":
            markdown_lines = []
            for raw_line in cell_lines:
                if raw_line.startswith("# "):
                    markdown_lines.append(raw_line[2:])
                elif raw_line == "#":
                    markdown_lines.append("")
                elif raw_line.startswith("#"):
                    markdown_lines.append(raw_line[1:])
                else:
                    markdown_lines.append(raw_line)
            source = "\\n".join(markdown_lines).strip("\\n")
        else:
            source = "\\n".join(cell_lines).rstrip()

        if not source:
            continue

        cell = {
            "cell_type": cell_type,
            "metadata": {},
            "source": [line + "\\n" for line in source.split("\\n")],
        }
        if cell_type == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

        notebook_cells.append(cell)

    return {
        "cells": notebook_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build_notebooks() -> int:
    count = 0
    for module_dir in sorted(ROOT.glob("module_*")):
        notebooks_dir = module_dir / "notebooks"
        notebooks_dir.mkdir(exist_ok=True)
        for script_path in sorted(module_dir.glob("[0-9][0-9]_*.py")):
            notebook = parse_percent_script(script_path)
            notebook_path = notebooks_dir / f"{script_path.stem}.ipynb"
            notebook_path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
            count += 1
    return count


if __name__ == "__main__":
    built = build_notebooks()
    print(f"Built {built} notebook(s).")
""",
    "tools/validate_course.py": """from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def validate() -> None:
    modules = sorted(ROOT.glob("module_*"))
    assert modules, "No modules found"

    lesson_count = 0
    notebook_count = 0
    exercise_count = 0

    for module_dir in modules:
        readme = module_dir / "README.md"
        assert readme.exists(), f"Missing {readme}"

        lessons = sorted(module_dir.glob("[0-9][0-9]_*.py"))
        notebooks = sorted((module_dir / "notebooks").glob("*.ipynb"))
        exercise_readmes = sorted(module_dir.glob("exercises/*/README.md"))

        assert lessons, f"No lessons in {module_dir.name}"
        assert len(lessons) == len(notebooks), f"Notebook mismatch in {module_dir.name}"
        assert exercise_readmes, f"No exercises in {module_dir.name}"

        for notebook in notebooks:
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            assert payload["nbformat"] == 4, f"Invalid nbformat in {notebook}"
            assert payload["cells"], f"Notebook without cells: {notebook}"

        lesson_count += len(lessons)
        notebook_count += len(notebooks)
        exercise_count += len(exercise_readmes)

    print(
        f"Validated {len(modules)} modules, {lesson_count} lessons, "
        f"{notebook_count} notebooks, {exercise_count} exercises."
    )


if __name__ == "__main__":
    validate()
""",
    "module_01_pythonic_foundations/__init__.py": "",
    "module_01_pythonic_foundations/README.md": """# Module 1 · Pythonic Foundations

Este módulo refuerza la forma idiomática de trabajar con variables, colecciones y datos de texto en Python.

## Lecciones

- `01_data_model_and_unpacking.py`: modelo de datos, mutabilidad, asignación múltiple y desempaque.
- `02_strings_collections_and_dates.py`: formateo, colecciones útiles y fechas con `datetime`.

## Ejercicios

- `exercises/lesson_01_student_snapshot/`
- `exercises/lesson_02_release_agenda/`
""",
    "module_01_pythonic_foundations/01_data_model_and_unpacking.py": """# %% [markdown]
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
""",
    "module_01_pythonic_foundations/02_strings_collections_and_dates.py": """# %% [markdown]
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
""",
    "module_01_pythonic_foundations/exercises/lesson_01_student_snapshot/README.md": """# Exercise · Student Snapshot

Completa `starter.py` para construir un resumen de estudiantes a partir de una
lista de tuplas.

## Objetivos

- Practicar desempaque.
- Identificar datos mutables e inmutables.
- Construir un diccionario final sin mutar la entrada original.

## Resultado esperado

La función debe retornar un diccionario con:

- `total_students`
- `tracks`
- `experience_average`
""",
    "module_01_pythonic_foundations/exercises/lesson_01_student_snapshot/starter.py": """def build_student_snapshot(records: list[tuple[str, str, int]]) -> dict:
    tracks = set()
    total_years = 0

    for record in records:
        name, track, years = record
        tracks.add(track)
        total_years += years

    return {
        "total_students": len(records),
        "tracks": sorted(tracks),
        "experience_average": round(total_years / len(records), 2) if records else 0,
    }


if __name__ == "__main__":
    sample = [
        ("Ana", "backend", 2),
        ("Luis", "data", 4),
        ("Marta", "backend", 3),
    ]
    print(build_student_snapshot(sample))
""",
    "module_01_pythonic_foundations/exercises/lesson_01_student_snapshot/solution.py": """def build_student_snapshot(records: list[tuple[str, str, int]]) -> dict:
    tracks = {track for _, track, _ in records}
    total_years = sum(years for _, _, years in records)

    return {
        "total_students": len(records),
        "tracks": sorted(tracks),
        "experience_average": round(total_years / len(records), 2) if records else 0,
    }


if __name__ == "__main__":
    sample = [
        ("Ana", "backend", 2),
        ("Luis", "data", 4),
        ("Marta", "backend", 3),
    ]
    print(build_student_snapshot(sample))
""",
    "module_01_pythonic_foundations/exercises/lesson_02_release_agenda/README.md": """# Exercise · Release Agenda

Implementa una función que reciba fechas en formato ISO y calcule la agenda de
publicación de un módulo.

## Objetivos

- Convertir texto a `date`.
- Calcular offsets de días.
- Formatear salida en un diccionario claro.
""",
    "module_01_pythonic_foundations/exercises/lesson_02_release_agenda/starter.py": """from datetime import date, timedelta


def build_release_agenda(start_date: str, lesson_count: int) -> dict:
    current = date.fromisoformat(start_date)
    schedule = [(current + timedelta(days=7 * index)).isoformat() for index in range(lesson_count)]
    return {
        "start_date": current.isoformat(),
        "lesson_count": lesson_count,
        "schedule": schedule,
    }


if __name__ == "__main__":
    print(build_release_agenda("2026-07-01", 4))
""",
    "module_01_pythonic_foundations/exercises/lesson_02_release_agenda/solution.py": """from datetime import date, timedelta


def build_release_agenda(start_date: str, lesson_count: int) -> dict:
    current = date.fromisoformat(start_date)
    schedule = [
        (current + timedelta(days=7 * lesson_index)).isoformat()
        for lesson_index in range(lesson_count)
    ]
    return {
        "start_date": current.isoformat(),
        "lesson_count": lesson_count,
        "schedule": schedule,
    }


if __name__ == "__main__":
    print(build_release_agenda("2026-07-01", 4))
""",
    "module_02_control_flow_and_comprehensions/__init__.py": "",
    "module_02_control_flow_and_comprehensions/README.md": """# Module 2 · Control Flow and Comprehensions

Este módulo se enfoca en escribir decisiones y recorridos de datos de forma
legible y eficiente.

## Lecciones

- `01_control_flow_patterns.py`
- `02_comprehensions_and_generators.py`

## Ejercicios

- `exercises/lesson_01_order_triage/`
- `exercises/lesson_02_event_digest/`
""",
    "module_02_control_flow_and_comprehensions/01_control_flow_patterns.py": """# %% [markdown]
# # 01. Patrones de control de flujo
#
# ## Objetivos
#
# - Escribir condicionales con reglas claras.
# - Evitar ramas innecesarias.
# - Usar guard clauses para reducir anidación.

# %%
orders = [
    {"id": 101, "total": 45, "status": "paid"},
    {"id": 102, "total": 5, "status": "pending"},
    {"id": 103, "total": 120, "status": "paid"},
]

# %% [markdown]
# ## Guard clauses
#
# Primero se resuelven los casos que bloquean el flujo normal.

# %%
def classify_order(order: dict) -> str:
    if order["status"] != "paid":
        return "blocked"
    if order["total"] >= 100:
        return "priority"
    if order["total"] >= 20:
        return "standard"
    return "low_value"


for order in orders:
    print(order["id"], classify_order(order))

# %% [markdown]
# ## `for` + acumuladores
#
# Todavía es un patrón útil cuando necesitas varias métricas al mismo tiempo.

# %%
priority_ids = []
blocked_ids = []

for order in orders:
    category = classify_order(order)
    if category == "priority":
        priority_ids.append(order["id"])
    elif category == "blocked":
        blocked_ids.append(order["id"])

print(priority_ids)
print(blocked_ids)

# %% [markdown]
# ## `match`
#
# En Python 3.10 puedes expresar reglas discretas de forma más directa cuando
# los casos dependen de patrones bien definidos.

# %%
def action_for_status(status: str) -> str:
    match status:
        case "paid":
            return "ship"
        case "pending":
            return "wait"
        case "cancelled":
            return "archive"
        case _:
            return "review"


print(action_for_status("paid"))
print(action_for_status("cancelled"))

# %% [markdown]
# ## Resumen
#
# - Las guard clauses simplifican la lectura.
# - Un buen acumulador evita múltiples recorridos innecesarios.
# - `match` funciona bien para reglas discretas.
""",
    "module_02_control_flow_and_comprehensions/02_comprehensions_and_generators.py": """# %% [markdown]
# # 02. Comprehensions y generadores
#
# ## Objetivos
#
# - Usar comprehensions cuando la transformación es simple.
# - Introducir generadores para no materializar datos innecesarios.

# %%
events = [
    {"user": "ana", "duration": 35, "status": "ok"},
    {"user": "luis", "duration": 12, "status": "retry"},
    {"user": "marta", "duration": 48, "status": "ok"},
    {"user": "ana", "duration": 20, "status": "ok"},
]

# %% [markdown]
# ## List comprehensions

# %%
successful_durations = [event["duration"] for event in events if event["status"] == "ok"]
print(successful_durations)

# %% [markdown]
# ## Dict comprehensions

# %%
latest_duration_by_user = {event["user"]: event["duration"] for event in events}
print(latest_duration_by_user)

# %% [markdown]
# ## Set comprehensions

# %%
active_users = {event["user"] for event in events if event["duration"] >= 20}
print(active_users)

# %% [markdown]
# ## Generadores
#
# Son una buena opción para procesar secuencias largas sin cargar todo en memoria.

# %%
def durations_over(limit: int):
    for event in events:
        if event["duration"] > limit:
            yield event["duration"]


for duration in durations_over(20):
    print(duration)

# %%
total_duration = sum(event["duration"] for event in events if event["status"] == "ok")
print(total_duration)

# %% [markdown]
# ## Resumen
#
# - Las comprehensions funcionan bien para una transformación puntual.
# - Los generadores ayudan a escalar el procesamiento.
""",
    "module_02_control_flow_and_comprehensions/exercises/lesson_01_order_triage/README.md": """# Exercise · Order Triage

Clasifica órdenes en `priority`, `standard`, `low_value` y `blocked`.

## Objetivos

- Practicar reglas con guard clauses.
- Consolidar acumuladores.
""",
    "module_02_control_flow_and_comprehensions/exercises/lesson_01_order_triage/starter.py": """def triage_orders(orders: list[dict]) -> dict:
    summary = {"priority": [], "standard": [], "low_value": [], "blocked": []}

    for order in orders:
        if order["status"] != "paid":
            summary["blocked"].append(order["id"])
        elif order["total"] >= 100:
            summary["priority"].append(order["id"])
        elif order["total"] >= 20:
            summary["standard"].append(order["id"])
        else:
            summary["low_value"].append(order["id"])

    return summary


if __name__ == "__main__":
    sample = [
        {"id": 1, "total": 150, "status": "paid"},
        {"id": 2, "total": 35, "status": "paid"},
        {"id": 3, "total": 8, "status": "paid"},
        {"id": 4, "total": 20, "status": "pending"},
    ]
    print(triage_orders(sample))
""",
    "module_02_control_flow_and_comprehensions/exercises/lesson_01_order_triage/solution.py": """def triage_orders(orders: list[dict]) -> dict:
    summary = {"priority": [], "standard": [], "low_value": [], "blocked": []}

    for order in orders:
        if order["status"] != "paid":
            summary["blocked"].append(order["id"])
            continue
        if order["total"] >= 100:
            summary["priority"].append(order["id"])
        elif order["total"] >= 20:
            summary["standard"].append(order["id"])
        else:
            summary["low_value"].append(order["id"])

    return summary


if __name__ == "__main__":
    sample = [
        {"id": 1, "total": 150, "status": "paid"},
        {"id": 2, "total": 35, "status": "paid"},
        {"id": 3, "total": 8, "status": "paid"},
        {"id": 4, "total": 20, "status": "pending"},
    ]
    print(triage_orders(sample))
""",
    "module_02_control_flow_and_comprehensions/exercises/lesson_02_event_digest/README.md": """# Exercise · Event Digest

Construye un resumen a partir de una lista de eventos.

## Objetivos

- Usar comprehensions.
- Resumir información en un solo paso.
""",
    "module_02_control_flow_and_comprehensions/exercises/lesson_02_event_digest/starter.py": """def build_event_digest(events: list[dict]) -> dict:
    ok_events = [event for event in events if event["status"] == "ok"]
    return {
        "ok_count": len(ok_events),
        "users": sorted({event["user"] for event in ok_events}),
        "total_duration": sum(event["duration"] for event in ok_events),
    }


if __name__ == "__main__":
    sample = [
        {"user": "ana", "duration": 30, "status": "ok"},
        {"user": "luis", "duration": 12, "status": "retry"},
        {"user": "ana", "duration": 15, "status": "ok"},
    ]
    print(build_event_digest(sample))
""",
    "module_02_control_flow_and_comprehensions/exercises/lesson_02_event_digest/solution.py": """def build_event_digest(events: list[dict]) -> dict:
    ok_events = [event for event in events if event["status"] == "ok"]
    return {
        "ok_count": len(ok_events),
        "users": sorted({event["user"] for event in ok_events}),
        "total_duration": sum(event["duration"] for event in ok_events),
    }


if __name__ == "__main__":
    sample = [
        {"user": "ana", "duration": 30, "status": "ok"},
        {"user": "luis", "duration": 12, "status": "retry"},
        {"user": "ana", "duration": 15, "status": "ok"},
    ]
    print(build_event_digest(sample))
""",
    "module_03_functions_and_functional_programming/__init__.py": "",
    "module_03_functions_and_functional_programming/README.md": """# Module 3 · Functions and Functional Programming

Aquí el foco es escribir funciones pequeñas, componibles y fáciles de probar.

## Lecciones

- `01_function_design.py`
- `02_higher_order_functions_and_decorators.py`

## Ejercicios

- `exercises/lesson_01_price_pipeline/`
- `exercises/lesson_02_retry_wrapper/`
""",
    "module_03_functions_and_functional_programming/01_function_design.py": """# %% [markdown]
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
# ## Resumen
#
# - Una función pequeña es más fácil de validar.
# - Un nombre claro comunica la intención.
# - `*args` y `**kwargs` deben usarse con criterio.
""",
    "module_03_functions_and_functional_programming/02_higher_order_functions_and_decorators.py": """# %% [markdown]
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
# ## `map` y `filter`

# %%
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
# ## Resumen
#
# - Una función puede ser un dato más dentro del programa.
# - Los decoradores permiten encapsular trazabilidad y validación.
""",
    "module_03_functions_and_functional_programming/exercises/lesson_01_price_pipeline/README.md": """# Exercise · Price Pipeline

Diseña una pequeña tubería de funciones para limpiar y transformar precios.
""",
    "module_03_functions_and_functional_programming/exercises/lesson_01_price_pipeline/starter.py": """def to_floats(values: list[str]) -> list[float]:
    return [float(value) for value in values]


def add_tax(values: list[float], tax_rate: float) -> list[float]:
    return [round(value * (1 + tax_rate), 2) for value in values]


def build_price_pipeline(values: list[str], tax_rate: float) -> list[float]:
    numeric_values = to_floats(values)
    return add_tax(numeric_values, tax_rate)


if __name__ == "__main__":
    print(build_price_pipeline(["10", "15.5", "20"], 0.19))
""",
    "module_03_functions_and_functional_programming/exercises/lesson_01_price_pipeline/solution.py": """def to_floats(values: list[str]) -> list[float]:
    return [float(value) for value in values]


def add_tax(values: list[float], tax_rate: float) -> list[float]:
    return [round(value * (1 + tax_rate), 2) for value in values]


def build_price_pipeline(values: list[str], tax_rate: float) -> list[float]:
    return add_tax(to_floats(values), tax_rate)


if __name__ == "__main__":
    print(build_price_pipeline(["10", "15.5", "20"], 0.19))
""",
    "module_03_functions_and_functional_programming/exercises/lesson_02_retry_wrapper/README.md": """# Exercise · Retry Wrapper

Implementa un decorador simple que reintente una función hasta `n` veces.
""",
    "module_03_functions_and_functional_programming/exercises/lesson_02_retry_wrapper/starter.py": """from functools import wraps


def retry(times: int):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            last_error = None
            for _ in range(times):
                try:
                    return function(*args, **kwargs)
                except ValueError as error:
                    last_error = error
            raise last_error

        return wrapper

    return decorator


if __name__ == "__main__":
    attempts = {"count": 0}

    @retry(3)
    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("not yet")
        return "ok"

    print(flaky())
""",
    "module_03_functions_and_functional_programming/exercises/lesson_02_retry_wrapper/solution.py": """from functools import wraps


def retry(times: int):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            last_error = None
            for _ in range(times):
                try:
                    return function(*args, **kwargs)
                except ValueError as error:
                    last_error = error
            raise last_error

        return wrapper

    return decorator


if __name__ == "__main__":
    attempts = {"count": 0}

    @retry(3)
    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("not yet")
        return "ok"

    print(flaky())
""",
    "module_04_files_serialization_and_paths/__init__.py": "",
    "module_04_files_serialization_and_paths/README.md": """# Module 4 · Files, Serialization and Paths

Este módulo baja la teoría a archivos reales usando sólo biblioteca estándar.

## Lecciones

- `01_pathlib_and_text_files.py`
- `02_csv_json_and_pickle.py`

## Ejercicios

- `exercises/lesson_01_log_summary/`
- `exercises/lesson_02_catalog_export/`
""",
    "module_04_files_serialization_and_paths/01_pathlib_and_text_files.py": """# %% [markdown]
# # 01. `pathlib` y archivos de texto
#
# ## Objetivos
#
# - Navegar rutas con `Path`.
# - Leer y escribir archivos de texto sin ambigüedades.

# %%
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOG_PATH = DATA_DIR / "sample_log.txt"

print(BASE_DIR.name)
print(LOG_PATH.exists())

# %% [markdown]
# ## Lectura segura

# %%
content = LOG_PATH.read_text(encoding="utf-8")
print(content.splitlines()[0])

# %% [markdown]
# ## Escritura controlada

# %%
report_path = DATA_DIR / "summary.txt"
line_count = len(content.splitlines())
report_path.write_text(f"Line count: {line_count}\\n", encoding="utf-8")
print(report_path.read_text(encoding="utf-8"))

# %% [markdown]
# ## Filtrar archivos

# %%
for path in sorted(DATA_DIR.glob("*.txt")):
    print(path.name)

# %% [markdown]
# ## Resumen
#
# - `Path` centraliza la lógica de rutas.
# - `read_text` y `write_text` resuelven muchos casos cotidianos.
""",
    "module_04_files_serialization_and_paths/02_csv_json_and_pickle.py": """# %% [markdown]
# # 02. CSV, JSON y pickle
#
# ## Objetivos
#
# - Leer y escribir formatos comunes.
# - Escoger el formato correcto según el uso.

# %%
import csv
import json
import pickle
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# %% [markdown]
# ## CSV

# %%
csv_path = DATA_DIR / "products.csv"
with csv_path.open(encoding="utf-8") as csv_file:
    rows = list(csv.DictReader(csv_file))

print(rows)

# %% [markdown]
# ## JSON

# %%
json_path = DATA_DIR / "products.json"
payload = {
    "items": rows,
    "total_items": len(rows),
}
json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.loads(json_path.read_text(encoding="utf-8"))["total_items"])

# %% [markdown]
# ## Pickle
#
# Útil para persistencia rápida interna, no para intercambio externo.

# %%
pickle_path = DATA_DIR / "products.pickle"
pickle_path.write_bytes(pickle.dumps(rows))
restored = pickle.loads(pickle_path.read_bytes())
print(restored[0]["name"])

# %% [markdown]
# ## Resumen
#
# - CSV para tablas simples.
# - JSON para interoperabilidad.
# - Pickle para snapshots internos de Python.
""",
    "module_04_files_serialization_and_paths/exercises/lesson_01_log_summary/README.md": """# Exercise · Log Summary

Lee un archivo de logs y retorna un resumen por nivel (`INFO`, `WARNING`,
`ERROR`).
""",
    "module_04_files_serialization_and_paths/exercises/lesson_01_log_summary/starter.py": """from pathlib import Path


def summarize_log(path: Path) -> dict:
    summary = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    for line in path.read_text(encoding="utf-8").splitlines():
        for level in summary:
            if line.startswith(level):
                summary[level] += 1
    return summary


if __name__ == "__main__":
    log_path = Path(__file__).resolve().parents[2] / "data" / "sample_log.txt"
    print(summarize_log(log_path))
""",
    "module_04_files_serialization_and_paths/exercises/lesson_01_log_summary/solution.py": """from pathlib import Path


def summarize_log(path: Path) -> dict:
    summary = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    for line in path.read_text(encoding="utf-8").splitlines():
        for level in summary:
            if line.startswith(level):
                summary[level] += 1
    return summary


if __name__ == "__main__":
    log_path = Path(__file__).resolve().parents[2] / "data" / "sample_log.txt"
    print(summarize_log(log_path))
""",
    "module_04_files_serialization_and_paths/exercises/lesson_02_catalog_export/README.md": """# Exercise · Catalog Export

Lee un CSV de productos y genera un JSON con el total de ítems y la suma del
inventario.
""",
    "module_04_files_serialization_and_paths/exercises/lesson_02_catalog_export/starter.py": """import csv
import json
from pathlib import Path


def export_catalog(csv_path: Path, json_path: Path) -> dict:
    with csv_path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    payload = {
        "total_items": len(rows),
        "inventory_units": sum(int(row["stock"]) for row in rows),
        "items": rows,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2] / "data"
    print(export_catalog(base / "products.csv", base / "catalog_export.json"))
""",
    "module_04_files_serialization_and_paths/exercises/lesson_02_catalog_export/solution.py": """import csv
import json
from pathlib import Path


def export_catalog(csv_path: Path, json_path: Path) -> dict:
    with csv_path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    payload = {
        "total_items": len(rows),
        "inventory_units": sum(int(row["stock"]) for row in rows),
        "items": rows,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2] / "data"
    print(export_catalog(base / "products.csv", base / "catalog_export.json"))
""",
    "module_05_oop_and_errors/__init__.py": "",
    "module_05_oop_and_errors/README.md": """# Module 5 · OOP and Errors

Este módulo muestra cómo modelar objetos pequeños y cómo comunicar fallos con
excepciones claras.

## Lecciones

- `01_classes_dataclasses_and_dunder.py`
- `02_exceptions_validation_and_custom_errors.py`

## Ejercicios

- `exercises/lesson_01_task_registry/`
- `exercises/lesson_02_payment_validation/`
""",
    "module_05_oop_and_errors/01_classes_dataclasses_and_dunder.py": """# %% [markdown]
# # 01. Clases, dataclasses y métodos especiales
#
# ## Objetivos
#
# - Modelar entidades simples con clases.
# - Reducir ruido con `@dataclass`.

# %%
from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    duration_minutes: int
    published: bool = False

    def publish(self) -> None:
        self.published = True


lesson = Lesson("Archivos con pathlib", 45)
print(lesson)
lesson.publish()
print(lesson)

# %% [markdown]
# ## Métodos especiales

# %%
class Cohort:
    def __init__(self, name: str, students: list[str]):
        self.name = name
        self.students = students

    def __len__(self) -> int:
        return len(self.students)

    def __repr__(self) -> str:
        return f"Cohort(name={self.name!r}, students={self.students!r})"


cohort = Cohort("Noche", ["Ana", "Luis", "Marta"])
print(cohort)
print(len(cohort))

# %% [markdown]
# ## Resumen
#
# - `dataclass` es excelente para modelos de datos.
# - Los métodos especiales mejoran la integración con Python.
""",
    "module_05_oop_and_errors/02_exceptions_validation_and_custom_errors.py": """# %% [markdown]
# # 02. Excepciones y validación
#
# ## Objetivos
#
# - Fallar con mensajes útiles.
# - Crear excepciones específicas cuando aporta claridad.

# %%
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
# ## Resumen
#
# - No todas las validaciones deben retornar `False`.
# - Una excepción específica hace más claro el error operacional.
""",
    "module_05_oop_and_errors/exercises/lesson_01_task_registry/README.md": """# Exercise · Task Registry

Crea una clase para registrar tareas y calcular cuántas están pendientes.
""",
    "module_05_oop_and_errors/exercises/lesson_01_task_registry/starter.py": """from dataclasses import dataclass


@dataclass
class Task:
    title: str
    completed: bool = False


class TaskRegistry:
    def __init__(self):
        self.tasks: list[Task] = []

    def add(self, task: Task) -> None:
        self.tasks.append(task)

    def pending_count(self) -> int:
        return sum(1 for task in self.tasks if not task.completed)


if __name__ == "__main__":
    registry = TaskRegistry()
    registry.add(Task("Notebook parity"))
    registry.add(Task("Exercise review", completed=True))
    print(registry.pending_count())
""",
    "module_05_oop_and_errors/exercises/lesson_01_task_registry/solution.py": """from dataclasses import dataclass


@dataclass
class Task:
    title: str
    completed: bool = False


class TaskRegistry:
    def __init__(self):
        self.tasks: list[Task] = []

    def add(self, task: Task) -> None:
        self.tasks.append(task)

    def pending_count(self) -> int:
        return sum(1 for task in self.tasks if not task.completed)


if __name__ == "__main__":
    registry = TaskRegistry()
    registry.add(Task("Notebook parity"))
    registry.add(Task("Exercise review", completed=True))
    print(registry.pending_count())
""",
    "module_05_oop_and_errors/exercises/lesson_02_payment_validation/README.md": """# Exercise · Payment Validation

Valida montos de pago y levanta una excepción clara cuando el valor no sea
aceptable.
""",
    "module_05_oop_and_errors/exercises/lesson_02_payment_validation/starter.py": """class PaymentValidationError(Exception):
    pass


def validate_payment(amount: float) -> float:
    if amount <= 0:
        raise PaymentValidationError("amount must be positive")
    return amount


if __name__ == "__main__":
    print(validate_payment(99.9))
""",
    "module_05_oop_and_errors/exercises/lesson_02_payment_validation/solution.py": """class PaymentValidationError(Exception):
    pass


def validate_payment(amount: float) -> float:
    if amount <= 0:
        raise PaymentValidationError("amount must be positive")
    return amount


if __name__ == "__main__":
    print(validate_payment(99.9))
""",
    "module_06_packages_and_sqlite/__init__.py": "",
    "module_06_packages_and_sqlite/exercises/__init__.py": "",
    "module_06_packages_and_sqlite/exercises/lesson_01_course_package/__init__.py": "",
    "module_06_packages_and_sqlite/exercises/lesson_02_library_queries/__init__.py": "",
    "module_06_packages_and_sqlite/README.md": """# Module 6 · Packages and SQLite

Este módulo cierra el curso con estructura de proyecto y persistencia local.

## Lecciones

- `01_packages_imports_and_cli.py`
- `02_sqlite_for_python_projects.py`

## Ejercicios

- `exercises/lesson_01_course_package/`
- `exercises/lesson_02_library_queries/`
""",
    "module_06_packages_and_sqlite/01_packages_imports_and_cli.py": """# %% [markdown]
# # 01. Paquetes, imports y CLI
#
# ## Objetivos
#
# - Entender cómo organizar código en módulos reutilizables.
# - Introducir una interfaz mínima por línea de comandos.

# %%
from module_06_packages_and_sqlite.shared.text_tools import slugify


title = "Curso de Python Intermedio"
print(slugify(title))

# %% [markdown]
# ## Punto de entrada simple

# %%
def main(name: str) -> None:
    print(f"Hola, {name}. Bienvenido al módulo final.")


if __name__ == "__main__":
    main("equipo")
""",
    "module_06_packages_and_sqlite/02_sqlite_for_python_projects.py": """# %% [markdown]
# # 02. SQLite para proyectos pequeños
#
# ## Objetivos
#
# - Leer y consultar una base SQLite desde Python.
# - Traducir resultados SQL a estructuras sencillas.

# %%
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "library.db"

with sqlite3.connect(DB_PATH) as connection:
    rows = connection.execute(
        (
            "SELECT category, COUNT(*) AS total_books "
            "FROM books "
            "GROUP BY category "
            "ORDER BY total_books DESC"
        )
    ).fetchall()

print(rows)

# %%
with sqlite3.connect(DB_PATH) as connection:
    expensive_books = connection.execute(
        "SELECT title, price FROM books WHERE price >= ? ORDER BY price DESC",
        (40,),
    ).fetchall()

print(expensive_books)

# %% [markdown]
# ## Resumen
#
# - SQLite es suficiente para proyectos educativos y herramientas locales.
# - Las consultas parametrizadas evitan errores y malas prácticas.
""",
    "module_06_packages_and_sqlite/shared/__init__.py": "",
    "module_06_packages_and_sqlite/shared/text_tools.py": """def slugify(value: str) -> str:
    return value.strip().lower().replace(" ", "-")
""",
    "module_06_packages_and_sqlite/exercises/lesson_01_course_package/README.md": """# Exercise · Course Package

Usa la función `slugify` para construir una lista de nombres técnicos para
módulos del curso.
""",
    "module_06_packages_and_sqlite/exercises/lesson_01_course_package/starter.py": """from module_06_packages_and_sqlite.shared.text_tools import slugify


def build_module_names(names: list[str]) -> list[str]:
    return [slugify(name) for name in names]


if __name__ == "__main__":
    print(build_module_names(["Python Foundations", "Files and JSON"]))
""",
    "module_06_packages_and_sqlite/exercises/lesson_01_course_package/solution.py": """from module_06_packages_and_sqlite.shared.text_tools import slugify


def build_module_names(names: list[str]) -> list[str]:
    return [slugify(name) for name in names]


if __name__ == "__main__":
    print(build_module_names(["Python Foundations", "Files and JSON"]))
""",
    "module_06_packages_and_sqlite/exercises/lesson_02_library_queries/README.md": """# Exercise · Library Queries

Consulta `library.db` y retorna los títulos cuyo precio sea mayor o igual al
valor recibido.
""",
    "module_06_packages_and_sqlite/exercises/lesson_02_library_queries/starter.py": """import sqlite3
from pathlib import Path


def expensive_titles(db_path: Path, minimum_price: float) -> list[str]:
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            "SELECT title FROM books WHERE price >= ? ORDER BY price DESC",
            (minimum_price,),
        ).fetchall()
    return [row[0] for row in rows]


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[2] / "data" / "library.db"
    print(expensive_titles(path, 40))
""",
    "module_06_packages_and_sqlite/exercises/lesson_02_library_queries/solution.py": """import sqlite3
from pathlib import Path


def expensive_titles(db_path: Path, minimum_price: float) -> list[str]:
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            "SELECT title FROM books WHERE price >= ? ORDER BY price DESC",
            (minimum_price,),
        ).fetchall()
    return [row[0] for row in rows]


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[2] / "data" / "library.db"
    print(expensive_titles(path, 40))
""",
}


TEXT_DATA: dict[str, str] = {
    "module_04_files_serialization_and_paths/data/sample_log.txt": """INFO Application started
WARNING Missing optional configuration
INFO Loading course modules
ERROR Failed to export notebook
INFO Retry completed
""",
    "module_04_files_serialization_and_paths/data/products.csv": """product_id,name,stock,price
1,Keyboard,12,35
2,Mouse,18,20
3,Monitor,6,180
""",
}


BOOKS = [
    ("Fluent Python", "python", 52.0),
    ("Architecture Patterns with Python", "architecture", 47.5),
    ("Automate the Boring Stuff", "python", 32.0),
    ("Designing Data-Intensive Applications", "data", 55.0),
]


def write_files() -> None:
    for relative_path, content in FILES.items():
        destination = COURSE_ROOT / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    for relative_path, content in TEXT_DATA.items():
        destination = COURSE_ROOT / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")


def create_library_db() -> None:
    db_path = COURSE_ROOT / "module_06_packages_and_sqlite" / "data" / "library.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL
            )
            """
        )
        connection.executemany(
            "INSERT INTO books (title, category, price) VALUES (?, ?, ?)",
            BOOKS,
        )
        connection.commit()


def build_notebooks() -> None:
    build_script = COURSE_ROOT / "tools" / "build_notebooks.py"
    namespace: dict[str, object] = {"__file__": str(build_script)}
    exec(build_script.read_text(encoding="utf-8"), namespace)
    namespace["build_notebooks"]()


def validate() -> None:
    validate_script = COURSE_ROOT / "tools" / "validate_course.py"
    namespace: dict[str, object] = {"__file__": str(validate_script)}
    exec(validate_script.read_text(encoding="utf-8"), namespace)
    namespace["validate"]()


def main() -> None:
    write_files()
    create_library_db()
    build_notebooks()
    validate()
    print(f"Scaffolded course at {COURSE_ROOT}")


if __name__ == "__main__":
    main()
