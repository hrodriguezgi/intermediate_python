# %% [markdown]
# # 01. `pathlib` y archivos de texto
#
# ## Objetivos
#
# - Navegar rutas con `Path`.
# - Leer y escribir archivos de texto sin ambigüedades.
# - Manejar encoding en el mundo real.
# - Asegurar limpieza de recursos con context managers.

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
report_path.write_text(f"Line count: {line_count}\n", encoding="utf-8")
print(report_path.read_text(encoding="utf-8"))

# %% [markdown]
# ## Filtrar archivos

# %%
for path in sorted(DATA_DIR.glob("*.txt")):
    print(path.name)

# %% [markdown]
# ## Encoding en el mundo real
#
# Los archivos del mundo real tienen problemas de encoding. UTF-8 no siempre funciona.

# %% [markdown]
# ### Problema: BOM en archivos Excel
#
# Archivos CSV exportados de Excel tienen un "Byte Order Mark" (BOM) al inicio.
# Si intentas leer con UTF-8 normal, ves caracteres raros en la primera celda.

# %%
# INCORRECTO: Lee el BOM como carácter
try:
    bad_content = LOG_PATH.read_text(encoding="utf-8")
    # Si el archivo tuviera BOM, la primera línea sería: '﻿LINE WITH BOM...'
except Exception as e:
    print(f"Error: {e}")

# CORRECTO: Usa utf-8-sig para ignorar BOM
good_content = LOG_PATH.read_text(encoding="utf-8-sig")
print("UTF-8-sig ignora el BOM correctamente")

# %% [markdown]
# ### Problema: Archivos legacy con encoding diferente
#
# Sistemas antiguos usan latin-1, cp1252 u otros encodings.
# Leer con UTF-8 falla con caracteres acentuados.

# %%
# Patrón: fallback graceful (intenta UTF-8, luego latin-1)
def read_file_safe(path: Path) -> str:
    """Lee archivo intentando múltiples encodings."""
    encodings = ["utf-8-sig", "utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise ValueError(f"No se pudo decodificar {path} con ningún encoding conocido")

content = read_file_safe(LOG_PATH)
print(f"Lectura exitosa con fallback: {len(content)} caracteres")

# %% [markdown]
# ### Detectar encoding automáticamente
#
# Para casos difíciles, usa `chardet` (requiere instalación).
# En datos ETL, esto ahorra horas de debugging.

# %%
# Simulación sin instalar chardet (solo concepto)
def detect_encoding(path: Path) -> str:
    """Detectaría encoding automáticamente con chardet."""
    # import chardet
    # raw = path.read_bytes()
    # detected = chardet.detect(raw)
    # return detected["encoding"]
    print("Concepto: chardet.detect() retorna el encoding detectado")
    return "utf-8"

# En producción:
# detected = detect_encoding(LOG_PATH)
# content = LOG_PATH.read_text(encoding=detected)

# %% [markdown]
# ## Context Managers: Por qué `with` es crítico
#
# Nunca hagas esto:

# %%
# ❌ INCORRECTO: El archivo podría quedar abierto si hay excepción
f = LOG_PATH.open(encoding="utf-8")
lines = f.readlines()
# Si process() falla, f.close() nunca se ejecuta -> file handle leak
# process(lines)
f.close()

# %% [markdown]
# `with` garantiza que el archivo se cierre **siempre**, incluso si hay excepciones.

# %%
# ✓ CORRECTO: El archivo se cierra automáticamente
with LOG_PATH.open(encoding="utf-8") as f:
    lines = f.readlines()
# Aquí el archivo ESTÁ CERRADO, incluso si process() falla
print(f"Lectura segura: {len(lines)} líneas")

# %% [markdown]
# ### Scenario real: Procesar millones de líneas
#
# Con `with`, puedes procesar línea por línea sin cargar todo en memoria.

# %%
# Iteración eficiente de un archivo grande
def process_log_stream(path: Path) -> int:
    """Cuenta líneas sin cargar todo el archivo."""
    count = 0
    with path.open(encoding="utf-8") as f:
        for line in f:
            # Procesa 1 línea a la vez
            if "ERROR" in line:
                count += 1
    return count

error_count = process_log_stream(LOG_PATH)
print(f"Errores encontrados: {error_count}")

# %% [markdown]
# ### ¿Qué pasa con recursos?
#
# - `with` cierra automáticamente (file handles, conexiones DB, sockets)
# - Sin `with`, los recursos quedan abiertos hasta garbage collection
# - En producción con miles de archivos, se agotan los file descriptors
# - Siempre usa `with` para archivos, conexiones, y locks

# %% [markdown]
# ## Resumen
#
# - `Path` centraliza la lógica de rutas.
# - `read_text` y `write_text` resuelven muchos casos cotidianos.
# - **Encoding real:** UTF-8-sig para Excel, fallback graceful para legacy
# - **Context managers:** Siempre usa `with` para archivos (exception safety)
# - **Streaming:** Para archivos grandes, itera línea por línea
