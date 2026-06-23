import sqlite3
from pathlib import Path


def expensive_titles(db_path: Path, minimum_price: float) -> list[str]:
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            "SELECT title FROM books WHERE price >= ? ORDER BY price DESC",
            (minimum_price,),
        ).fetchall()
    return [row[0] for row in rows]


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[2] / "data" / "library.db"
    print(expensive_titles(path, 40))
