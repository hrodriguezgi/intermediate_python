# Module 0 · Python Refresh

Este módulo repasa conceptos base de Python para arrancar el curso con un
lenguaje común sobre tipos de datos, estructuras y operaciones esenciales.
Incluye mejoras prácticas y orientadas a data engineering: rendimiento,
validación defensiva y datos desordenados.

## Lecciones

### Foundational Content

- **`01_data_types_and_variables.py`**
  - Tipos numéricos, booleanos, strings
  - Variables y reasignación
  - Conversión entre tipos
  - Truthy/falsy
  - None vs Empty Containers (gotchas importantes en validación)

- **`02_core_data_structures.py`**
  - Listas, tuplas, diccionarios, conjuntos
  - Queue con `deque` y stack simples
  - Recorrido de estructuras
  - Elegir la estructura correcta (performance matters)
  - Los datos reales son desordenados (validación defensiva)

## Ejercicios

### Core Skills (Lessons 01-02)

- **`exercises/lesson_01_student_record/`**
  - Iteración sobre listas de diccionarios
  - Conversión de tipos (`int()`)
  - Normalización de strings (`.strip()`, `.title()`)

- **`exercises/lesson_02_inventory_summary/`**
  - Acumulación de valores numéricos
  - Conjuntos para unicidad
  - Diccionarios de agregación

### Supplementary Content (Lessons 03-04)

- **`exercises/lesson_03_structure_performance/`**
  - Deduplicación con list vs set en 100K items
  - Benchmark con `timeit`: ~14,500x speedup con set
  - Real scenario: ETL pipelines con datasets masivos
  - **Objetivo:** Entender implicaciones de rendimiento

- **`exercises/lesson_04_defensive_data_handling/`**
  - Funciones defensivas: `safe_parse_int()`, `safe_parse_bool()`
  - None vs empty containers en configuración
  - Parsing de CSV y APIs con tipos inconsistentes
  - **Objetivo:** Prepararse para datos reales desordenados

## Conceptos Clave

| Concepto | Lección | Ejercicio | Impacto |
|----------|---------|-----------|--------|
| Data Structure Performance | 02 | 03 | 14,500x speedup posible |
| None vs Empty Containers | 01 | 04 | Evita bugs silenciosos |
| Mixed-Type Handling | 02 | 04 | Crítico para APIs/CSVs |
| Type Validation | 01 | 04 | Production-ready patterns |
