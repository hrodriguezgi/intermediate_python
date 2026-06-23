# %% [markdown]
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
report_path.write_text(f"Line count: {line_count}\n", encoding="utf-8")
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
