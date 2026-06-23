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
├── tools/
│   ├── build_notebooks.py
│   └── validate_course.py
├── module_00_python_refresh/
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

## Patrones Real-World Incluidos

Este curso enfatiza situaciones que encontrarás en producción:

- **Datos desordenados:** Archivos con diferentes encodings, CSVs con formatos variados, respuestas de APIs con tipos mixtos
- **Rendimiento:** Elección de estructuras de datos por complejidad (list vs set para búsquedas), generators vs comprehensions para archivos grandes
- **Errores defensivos:** Excepciones con contexto, validación de entrada, manejo seguro de conexiones
- **Seguridad:** Consultas SQL parametrizadas, prevención de inyecciones, manejo de credenciales
- **Concurrencia:** Transacciones, context managers, bloqueos de recursos
- **Patrones reusables:** Decoradores prácticos, composición vs herencia, funciones puras

## Últimas Mejoras

Todas las mejoras recientes enfatizan **situaciones reales** que rompen código de estudiantes:
- Gotchas de copias superficiales en colecciones anidadas
- Operador walrus (`:=`) para validación en loops
- Match statements para procesamiento de eventos
- Generators para archivos de gigabytes
- Encoding edge cases (BOM, latin-1)
- Custom exceptions con contexto completo
- Transactions y SQL injection en SQLite

Ver [MODULE_IMPROVEMENTS.md](./MODULE_IMPROVEMENTS.md) para detalles de cada mejora.

## Utilidades

```bash
uv run python tools/build_notebooks.py
uv run python tools/validate_course.py
uv run python -m module_00_python_refresh.01_data_types_and_variables
uv run python -m module_01_pythonic_foundations.01_data_model_and_unpacking
uv run python -m module_06_packages_and_sqlite.01_packages_imports_and_cli
uv run ruff check .
uv run ruff format .
uv run flake8 .
```

## Documentación Importante

- **[CLAUDE.md](./CLAUDE.md)** — Guía completa de desarrollo: filosofía del curso, rol del instructor, patrones enseñados, y flujo de trabajo.
- **[MODULE_IMPROVEMENTS.md](./MODULE_IMPROVEMENTS.md)** — Plan detallado de mejoras por módulo con ejemplos de código real-world, prioridades, y estrategia de implementación.

## Convenciones

- Usa `Python 3.12` para evitar incompatibilidades con `match` y otras features modernas.
- Prefiere imports absolutos dentro del paquete cuando una lección reutiliza código de otro archivo.
- Ejecuta scripts de módulos y ejercicios desde la raíz del repo con `uv run python -m ...`.
- Las lecciones enfatizan **mostrar el problema primero** antes de la solución, con escenarios reales y trade-offs explicados.
