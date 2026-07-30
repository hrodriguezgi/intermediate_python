# Module 6 · Databases (SQLite & DuckDB with SQLAlchemy)

Manejo de datos persistentes con bases de datos reales en Python.

## Lecciones

### 01. SQLAlchemy Fundamentals
**Temas:** ORM basics, modelos, sesiones, queries en Python
- ¿Por qué SQLAlchemy?
- Definir modelos con ORM
- Crear, leer, actualizar datos
- Context managers para sesiones

**Aprendes:** Abstracción SQL con Python objects

### 02. SQLite con SQLAlchemy  
**Temas:** Transacciones, ACID, seguridad, error handling
- Cuándo usar SQLite vs otras bases de datos
- Transacciones (todo o nada)
- Prevención de SQL injection
- Manejo de errores (IntegrityError, OperationalError)
- Caso real: transferencias de dinero, órdenes atómicas

**Aprendes:** Datos consistentes, operaciones seguras

### 03. DuckDB para Analytics
**Temas:** Analytics en memoria, queries rápidas, performance
- SQLite vs DuckDB: trade-offs
- Cargar CSV sin intermediarios
- Queries analíticas (GROUP BY, JOIN, agregaciones)
- Comparación de performance
- Cuándo usar cada tecnología

**Aprendes:** Análisis rápido de datos, elección de herramienta correcta

### 04. PostgreSQL con SQLAlchemy
**Temas:** Bases de datos empresariales, conexiones en red, producción
- PostgreSQL vs SQLite: cuándo usar cada una
- Connection pooling para múltiples conexiones concurrentes
- Transacciones en servidor real
- Error handling específico de PostgreSQL
- Queries avanzadas (JOINs, agregaciones, funciones)
- Setup en Mac con Homebrew

**Aprendes:** Conectar a bases de datos de producción, escalabilidad

## Ejercicios

- `exercises/lesson_01_course_package/` - Estructura de paquetes
- `exercises/lesson_02_library_queries/` - Queries a SQLite

## Proyecto Final

Ver `final_project/` en la raíz del curso:
- Cargar CSV → Validar → SQLite → DuckDB → FastAPI
- Aplicar todo el módulo en contexto real

## Ejecutar

```bash
# Lesson 1: SQLAlchemy basics
python -m module_06_packages_and_sqlite.01_sqlalchemy_fundamentals

# Lesson 2: SQLite transactions
python -m module_06_packages_and_sqlite.02_sqlite_with_sqlalchemy

# Lesson 3: DuckDB analytics
python -m module_06_packages_and_sqlite.03_duckdb_for_analytics

# Lesson 4: PostgreSQL (requiere PostgreSQL instalado)
# ANTES: Cambiar POSTGRES_PASSWORD en el archivo
python -m module_06_packages_and_sqlite.04_postgresql_with_sqlalchemy
```

## Concepto Clave

**Seguridad + Performance + Persistencia**

- ORM previene SQL injection automáticamente
- Transacciones garantizan consistencia
- DuckDB es 10-100x más rápido que SQLite para analytics
- Elegir la herramienta correcta importa

## Requisitos

```
sqlalchemy>=2.0
duckdb>=0.8
psycopg2-binary>=2.9  # Para PostgreSQL
```

**Instalación en Mac:**
```bash
# PostgreSQL server
brew install postgresql@16
brew services start postgresql@16

# Python driver
pip install psycopg2-binary
# O con uv
uv pip install psycopg2-binary
```

## Siguiente

→ Module 07: FastAPI (Exponer datos vía API)
