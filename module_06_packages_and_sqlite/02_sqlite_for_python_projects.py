# %% [markdown]
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
        "SELECT category, COUNT(*) AS total_books "
        "FROM books "
        "GROUP BY category "
        "ORDER BY total_books DESC"
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
