from datetime import date, timedelta
from collections import Counter


## Ejercicio 1: Construir un resumen de estudiantes
def build_student_snapshot(records: list[tuple[str, str, int]]) -> dict:
    """
    Construye un resumen estadístico de estudiantes a partir de registros de tuplas.

    Args:
        records: Lista de tuplas (nombre, track, años_experiencia)

    Returns:
        Diccionario con total_students, tracks ordenados, y experience_average
    """
    # TODO: Implementa la función aquí


## Ejercicio 2: Construir un calendario de lanzamientos
def build_release_agenda(start_date: str, lesson_count: int) -> dict:
    """
    Construye un calendario de publicación de lecciones.

    Args:
        start_date: Fecha de inicio en formato ISO (ej: "2026-07-01")
        lesson_count: Número de lecciones a programar

    Returns:
        Diccionario con start_date, lesson_count, y schedule (lista de fechas ISO)
    """
    # TODO: Implementa la función aquí


## Ejercicio 3: Normalizar y contar tags
def normalize_and_count_tags(tags_string: str) -> dict:
    """
    Normaliza tags desordenados y cuenta sus frecuencias.

    Args:
        tags_string: String con tags separados por comas (puede tener espacios, mayúsculas, duplicados)

    Returns:
        Diccionario con:
        - unique_tags: lista ordenada de tags únicos
        - total_unique: cantidad de tags únicos
        - frequencies: diccionario con contador de cada tag
    """
    # TODO: Implementa la función aquí


if __name__ == "__main__":
    ## Ejercicio 1:
    print("\n" + "=" * 50)
    print("Ejercicio 1: Construir un resumen de estudiantes")
    sample = [
        ("Ana", "backend", 2),
        ("Luis", "data", 4),
        ("Marta", "backend", 3),
    ]
    result = build_student_snapshot(sample)
    print(result, "\n")

    ## Ejercicio 2:
    print("\n" + "=" * 50)
    print("Ejercicio 2: Construir un calendario de lanzamientos")
    print(build_release_agenda("2026-07-01", 4))

    ## Ejercicio 3:
    print("\n" + "=" * 50)
    print("Ejercicio 3: Normalizar y contar tags")
    messy_tags = "python, Data , PYTHON,  files,python,data"
    result = normalize_and_count_tags(messy_tags, "\n")

    print("Normalized tags:")
    print(f"  Unique: {result['unique_tags']}")
    print(f"  Total unique: {result['total_unique']}")
    print(f"  Frequencies: {result['frequencies']}")

    # Verificaciones
    assert result["total_unique"] == 3, "Should have 3 unique tags"
    assert result["unique_tags"] == ["data", "files", "python"], "Should be sorted"
    assert result["frequencies"]["python"] == 3, "Python appears 3 times"
