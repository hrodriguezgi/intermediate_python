# %% [markdown]
# # 02. CSV, JSON y pickle
#
# ## Objetivos
#
# - Leer y escribir formatos comunes.
# - Escoger el formato correcto según el uso.
# - Procesar archivos grandes sin cargar todo en memoria.
# - Manejar variaciones reales de CSV (delimitadores, encodings).

# %%
import csv
import json
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# %% [markdown]
# ## CSV: Lectura básica

# %%
csv_path = DATA_DIR / "products.csv"
print(csv_path.exists())

# %%
with csv_path.open(encoding="utf-8") as csv_file:
    rows = list(csv.DictReader(csv_file))

print(rows)

# %% [markdown]
# ## Streaming: Procesar archivos grandes
#
# **Problema:** `list(csv.DictReader(...))` carga TODO en memoria.
# Para un CSV de 10GB, esto falla.

# %%
#  INCORRECTO: Carga todo en memoria
# rows = list(csv.DictReader(csv_file))  # 10GB CSV -> crash

# %% [markdown]
# ### Solución: Itera fila por fila


# %%
#  CORRECTO: Procesa 1 fila a la vez, memoria constante
def process_csv_stream(path: Path) -> int:
    """Procesa CSV línea por línea sin cargar en memoria."""
    total_items = 0
    with path.open(encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Procesa 1 fila, descarta, siguiente
            total_items += 1
            if total_items <= 2:
                print(f"Fila {total_items}: {row}")

    return total_items


total = process_csv_stream(csv_path)
print(f"Total procesado: {total} filas")

# %% [markdown]
# ### Scenario real: Procesar millones de registros
#
# En ETL, típicamente transformas y guardas en otra fuente:


# %%
def etl_pipeline(csv_path: Path, output_path: Path) -> int:
    """Lee CSV grande, transforma, escribe sin cargar en memoria."""
    count = 0
    with csv_path.open("r", encoding="utf-8") as infile:
        with output_path.open("w", encoding="utf-8") as outfile:
            reader = csv.DictReader(infile)
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row in reader:
                # Transforma
                if "price" in row:
                    try:
                        row["price"] = float(row["price"]) / 2
                    except ValueError:
                        row["price"] = 0.0
                # Escribe
                writer.writerow(row)
                count += 1

    return count


output_csv = DATA_DIR / "products_transformed.csv"
processed = etl_pipeline(csv_path, output_csv)
print(f"Pipeline: {processed} filas transformadas")

# %% [markdown]
# ## CSV: Variaciones reales
#
# Datos del mundo real tienen diferentes delimitadores, codificaciones, etc.

# %% [markdown]
# ### Problema: CSV europeo usa punto-y-coma

# %%
# Datos simulados con delimitador semicolon (Excel europeo)
european_csv_content = """nombre;edad;ciudad
Ana;30;Madrid
Bob;25;Barcelona"""

euro_path = DATA_DIR / "european.csv"
euro_path.write_text(european_csv_content, encoding="utf-8")

#  INCORRECTO: Asume comma como delimitador
with euro_path.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    wrong_rows = list(reader)
    print("Con comma (INCORRECTO):", wrong_rows[0])

#  CORRECTO: Especifica el delimitador
with euro_path.open(encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    correct_rows = list(reader)
    print("Con semicolon (CORRECTO):", correct_rows[0])

# %% [markdown]
# ### Variaciones comunes de CSV
#
# Real CSV files use different delimiters:
# - **Comma** (`,`) — USA standard
# - **Semicolon** (`;`) — Europe (Excel)
# - **Tab** (`\t`) — Tab-separated values
# - **Pipe** (`|`) — Legacy systems
#
# Always combine with encoding handling for robustness.

# %% [markdown]
# ### Encoding + Dialect juntos


# %%
# Encoding + dialect juntos (real scenario)
def read_csv_flexible(path: Path, delimiter: str = ",", encoding: str = "utf-8"):
    """Lee CSV con flexibilidad en delimitador y encoding."""
    with path.open(encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader)


# Ejemplo: CSV tabulado con latin-1 encoding
tab_path = DATA_DIR / "tab_separated.txt"
tab_path.write_text("id\tnombre\nidad\n1\tAlice\n2\tBob", encoding="utf-8")

# Lee con delimitador TAB
flexible_rows = read_csv_flexible(tab_path, delimiter="\t")
print(f"Lectura flexible: {flexible_rows[0]}")

# %% [markdown]
# ## JSON: Serialización de datos estructurados
#
# **Úsalo para:**
# - APIs (intercambio entre sistemas)
# - Web services (REST, GraphQL)
# - Datos que otros lenguajes necesitan leer
# - Configuración básica (aunque TOML es mejor)

# %%
# Métodos JSON: string vs file

# %% [markdown]
# ### `dumps()` vs `dump()` — String vs File
#
# | Método | Qué hace | Retorna | Uso |
# |--------|----------|---------|-----|
# | `json.dumps()` | Serializa a **string** | str | Enviar por red, logging, APIs |
# | `json.dump()` | Serializa a **archivo** | nada | Guardar en disco |
# | `json.loads()` | Deserializa **string** | dict/list | Recibir de API, parsear JSON en string |
# | `json.load()` | Deserializa **archivo** | dict/list | Leer de disco |

# %%
payload = {
    "items": rows if rows else [{"name": "Sample", "price": "9.99"}],
    "total_items": len(rows) if rows else 1,
}

# %% [markdown]
# ### Opción 1: String (dumps/loads)

# %%
# Serializar a string
json_string = json.dumps(payload, ensure_ascii=False, indent=2)
print(f"JSON como string ({len(json_string)} caracteres):")
print(json_string[:100] + "...")

# Deserializar desde string
parsed = json.loads(json_string)
print(f"Parseado: {parsed['total_items']} items")

# %% [markdown]
# **Caso de uso:** APIs, logging, enviar por red


# %%
# Ejemplo: Respuesta de API
def api_response(data: dict) -> str:
    """Retorna JSON como string para HTTP response."""
    return json.dumps(data, ensure_ascii=False)


response = api_response(payload)
print(f"API response: {response[:50]}...")

# %% [markdown]
# ### Opción 2: Archivo (dump/load)

# %%
# Guardar directamente a archivo
json_path = DATA_DIR / "products2.json"
with json_path.open("w", encoding="utf-8") as file:
    json.dump(payload, file, ensure_ascii=False, indent=2)

print(f"Guardado en: {json_path.name}")

# %%
# Leer directamente desde archivo
with json_path.open("r", encoding="utf-8") as f:
    loaded = json.load(f)

print(f"Cargado: {loaded['total_items']} items")

# %% [markdown]
# **Caso de uso:** Guardar/cargar archivos en disco

# %% [markdown]
# ### Comparación: String vs File

# %%
print("Métodos JSON:")
print("- dumps/loads: String ↔ Python (para APIs, logging)")
print("- dump/load: Archivo ↔ Python (para almacenamiento)")
print()

# Mejor práctica: combinados
print("Mejor práctica: usa dump/load para archivos")
with json_path.open("w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

print(" Más eficiente que: json_string = json.dumps(...)")
print("                    path.write_text(json_string)")

# %% [markdown]
# ## Pickle: Serialización de objetos Python
#
# **Úsalo SOLO para:**
# - Cache interno (datos computados que necesitas reutilizar)
# - Estado de aplicación (no intercambio externo)
# - ML models (después del entrenamiento)
#
# **NUNCA lo uses para:**
# - Datos de usuarios (security risk)
# - Intercambio con otros sistemas (solo entiende Python)
# - Datos no confiables (arbitrary code execution)

# %%
pickle_path = DATA_DIR / "products.pickle"
pickle_path.write_bytes(pickle.dumps(rows))
restored = pickle.loads(pickle_path.read_bytes())
if restored:
    print(restored[0].get("name", "No name"))
else:
    print("No data in pickle")

# %% [markdown]
# ### Scenario real: Cache de resultados computados

# %%
import time
from datetime import datetime


def expensive_computation(data: list) -> dict:
    """Simulación de cálculo costoso (ej: ML prediction)."""
    time.sleep(0.1)  # Simula trabajo pesado
    return {
        "result": sum(int(row.get("stock", 0)) for row in data),
        "computed_at": datetime.now().isoformat(),
    }


# Sin cache: recalcula cada vez (lento)
result1 = expensive_computation(rows)
print(f"Sin cache: {result1}")

# Con pickle cache: guarda resultado, reutiliza
cache_path = DATA_DIR / "computation_cache.pickle"

# Primera vez: calcula y guarda
if not cache_path.exists():
    result = expensive_computation(rows)
    cache_path.write_bytes(pickle.dumps(result))
    print(f"Cache creado: {result}")
else:
    # Uso posterior: recupera del cache (instant)
    cached_result = pickle.loads(cache_path.read_bytes())
    print(f"Cache hit (instant): {cached_result}")

# %% [markdown]
# ### Scenario real: Serializar modelos ML
#
# ```python
# # Entrenar modelo (tarda minutos)
# model = train_model(training_data)
#
# # Guardar con pickle
# model_path = Path("trained_model.pickle")
# model_path.write_bytes(pickle.dumps(model))
#
# # En producción: cargar y predecir (instant)
# model = pickle.loads(model_path.read_bytes())
# prediction = model.predict(new_data)
# ```

# %% [markdown]
# ## TOML: Configuración moderna
#
# Python 3.11+ tiene `tomllib` built-in. Mejor que JSON para configs.
# - Soporta comentarios
# - Más legible que JSON
# - Tipos de datos nativos (bool, int, strings)
# - Sin comillas innecesarias

# %%
import tomllib

# Archivo TOML (legible, permite comentarios)
toml_content = """
# Configuración de la aplicación

[database]
host = "localhost"
port = 5432
user = "admin"
password = "secret123"  # NUNCA dejes passwords en repo
debug = true

[cache]
ttl = 3600  # 1 hora en segundos
enabled = true
backends = ["redis", "memcached"]

[logging]
level = "INFO"
file = "/var/log/app.log"
"""

toml_path = DATA_DIR / "config.toml"
toml_path.write_text(toml_content, encoding="utf-8")

# Lee TOML
with toml_path.open("rb") as f:
    config = tomllib.load(f)
    print(f"Config database: {config['database']['host']}")
    print(f"Cache backends: {config['cache']['backends']}")

# %% [markdown]
# ### Scenario real: Configuración de aplicación ETL
#
# ```toml
# # pyproject.toml o config.toml
# [etl]
# batch_size = 10000
# timeout_seconds = 300
# retry_attempts = 3
#
# [sources.csv]
# path = "data/input.csv"
# delimiter = ";"
# encoding = "utf-8-sig"
#
# [sources.database]
# host = "prod-db.internal"
# port = 5432
# pool_size = 20
#
# [output]
# format = "json"
# destination = "s3://bucket/output/"
# ```

# %% [markdown]
# ### Comparación: JSON vs TOML

# %%
import json

# Mismo config en JSON (vs TOML arriba)
json_config = {
    "etl": {
        "batch_size": 10000,
        "timeout_seconds": 300,
        "retry_attempts": 3,
    },
    "sources": {
        "csv": {
            "path": "data/input.csv",
            "delimiter": ";",
            "encoding": "utf-8-sig",
        }
    },
}

print("\nJSON (verbose, sin comentarios):")
print(json.dumps(json_config, indent=2)[:150] + "...")

# TOML es más legible, especialmente para configuración grande

# %% [markdown]
# ## Resumen
#
# - **CSV para tablas:** Pero cuidado con encoding y delimitadores
# - **Streaming:** Para archivos grandes, itera fila por fila
# - **JSON para interoperabilidad:** APIs, web services
# - **Pickle para snapshots internos:** Solo Python-a-Python
# - **TOML para configuración:** Moderno, legible, comentarios permitidos
