# Intermediate Python

Curso práctico de Python intermedio orientado a escribir código más expresivo, mantenible y útil para proyectos reales.

Este curso enfatiza **patrones reales** que encontrarás en producción: manejo de datos desordenados, casos extremos, problemas de rendimiento, y cómo escribir código defensivo que sobreviva en el mundo real.

## Objetivos

- Consolidar bases sólidas de Python más allá de la sintaxis inicial.
- Practicar diseño de funciones, manejo de archivos, serialización, POO y SQLite.
- Entender patrones reales: rendimiento, seguridad, manejo de errores, y datos desordenados.
- Aprender de gotchas comunes en pipelines de datos, APIs, y procesamiento de archivos.
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
├── CLAUDE.md
├── MODULE_IMPROVEMENTS.md
├── tools/
│   ├── build_notebooks.py
│   └── validate_course.py
├── module_00_python_refresh/
├── module_01_pythonic_foundations/
├── module_02_control_flow_and_comprehensions/
├── module_03_functions_and_functional_programming/
├── module_04_files_serialization_and_paths/
├── module_05_oop_and_errors/
├── module_06_packages_and_sqlite/       (Databases: SQLite & DuckDB)
├── module_07_fastapi/                   (FastAPI: REST APIs)
└── final_project/                       (Capstone: Complete application)
```

## Flujo recomendado

**Módulos 0-5:**
1. Leer el `README.md` del módulo.
2. Ejecutar la lección con `uv run` usando el módulo Python.
3. Repasar el notebook equivalente en `notebooks/`.
4. Resolver el ejercicio correspondiente en `exercises/`.

**Módulo 6-7 + Final Project:**
1. Leer las lecciones (01, 02, 03) de cada módulo.
2. Ejecutar cada lección para entender los conceptos.
3. Completar el **Proyecto Final** (ver abajo) que integra todo.

### Proyecto Final: Capstone Application

**Ubicación:** `final_project/`

Build a complete E-Commerce Inventory Management System que integra los 7 módulos:

| Phase | Modules | What |
|-------|---------|------|
| 1 | 0, 4 | Load & validate CSV files |
| 2 | 5 | Define ORM models + Pydantic validation |
| 3 | 6 | SQLite with transactions (ACID) |
| 4 | 6 | DuckDB for analytics (fast queries) |
| 5 | 7 | FastAPI REST API (CRUD + analytics) |
| 6 | All | Testing & documentation |

**Start:** `cd final_project && python 01_data_loading.py`

**Time:** ~5-6 hours (self-paced)

## Setup

```bash
uv sync --group dev
```

## Patrones Real-World Incluidos

Este curso enfatiza situaciones que encontrarás en producción:

- **Datos desordenados:** Archivos con diferentes encodings, CSVs con formatos variados, respuestas de APIs con tipos mixtos
- **Rendimiento:** Elección de estructuras de datos por complejidad (list vs set para búsquedas), generators vs comprehensions para archivos grandes
- **Errores defensivos:** Excepciones con contexto, validación de entrada, manejo seguro de conexiones
- **Seguridad:** Consultas SQL parametrizadas, prevención de inyecciones, manejo de credenciales
- **Concurrencia:** Transacciones, context managers, bloqueos de recursos
- **Patrones reusables:** Decoradores prácticos, composición vs herencia, funciones puras

## Módulos Incluidos

### Módulos 0-5: Python Fundamentals
- **Module 0:** Tipos de datos, estructuras, performance
- **Module 1:** Pythonic code, mutabilidad, unpacking
- **Module 2:** Control flow, comprehensions, match statements
- **Module 3:** Functions, decorators, generators
- **Module 4:** Files, CSV, JSON, encoding, streaming
- **Module 5:** OOP, dataclasses, custom exceptions

### Módulo 6: Databases (SQLite & DuckDB)
- **Lesson 1:** SQLAlchemy ORM fundamentals
- **Lesson 2:** SQLite transactions, ACID, security, error handling
- **Lesson 3:** DuckDB analytics (in-memory SQL, 10-100x faster)

### Módulo 7: FastAPI
- **Lesson 1:** REST endpoints, type hints, Swagger UI
- **Lesson 2:** Database integration, dependency injection, CRUD
- **Lesson 3:** Pydantic validation, custom validators

### Final Project
- Complete end-to-end data application
- Integrates all 7 modules
- 5-6 hours hands-on coding
- Realistic scenarios

## Últimas Mejoras

Todas las mejoras recientes enfatizan **situaciones reales** que rompen código de estudiantes:
- Gotchas de copias superficiales en colecciones anidadas
- Operador walrus (`:=`) para validación en loops
- Match statements para procesamiento de eventos
- Generators para archivos de gigabytes
- Encoding edge cases (BOM, latin-1)
- Custom exceptions con contexto completo
- Transactions y SQL injection en SQLite
- SQLAlchemy ORM + DuckDB para analytics
- FastAPI con validación automática

Ver [MODULE_IMPROVEMENTS.md](./MODULE_IMPROVEMENTS.md) para detalles de cada mejora.

## Utilidades

```bash
# Build Jupyter notebooks from Python scripts
uv run python tools/build_notebooks.py

# Validate course structure
uv run python tools/validate_course.py

# Run specific lessons
uv run python -m module_00_python_refresh.01_data_types_and_variables
uv run python -m module_01_pythonic_foundations.01_data_model_and_unpacking
uv run python -m module_04_files_serialization_and_paths.01_pathlib_and_text_files
uv run python -m module_06_packages_and_sqlite.01_sqlalchemy_fundamentals
uv run python -m module_06_packages_and_sqlite.02_sqlite_with_sqlalchemy
uv run python -m module_06_packages_and_sqlite.03_duckdb_for_analytics

# Run Final Project
cd final_project
python 01_data_loading.py
python 02_database_models.py
python 03_sqlite_operations.py
python 04_duckdb_analytics.py
uvicorn 05_fastapi_application:app --reload  # Then visit http://localhost:8000/docs

# Code quality
uv run ruff check .
uv run ruff format .
```

## Documentación Importante

- **[CLAUDE.md](./CLAUDE.md)** — Guía completa de desarrollo: filosofía del curso, rol del instructor, patrones enseñados, y flujo de trabajo.
- **[MODULE_IMPROVEMENTS.md](./MODULE_IMPROVEMENTS.md)** — Plan detallado de mejoras por módulo con ejemplos de código real-world, prioridades, y estrategia de implementación.

## Convenciones

- Usa `Python 3.12` para evitar incompatibilidades con `match` y otras features modernas.
- Prefiere imports absolutos dentro del paquete cuando una lección reutiliza código de otro archivo.
- Ejecuta scripts de módulos y ejercicios desde la raíz del repo con `uv run python -m ...`.
- Las lecciones enfatizan **mostrar el problema primero** antes de la solución, con escenarios reales y trade-offs explicados.
