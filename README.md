# Intermediate Python

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
