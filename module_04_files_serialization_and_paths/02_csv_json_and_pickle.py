# %% [markdown]
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
json_path.write_text(
    json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
)
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
