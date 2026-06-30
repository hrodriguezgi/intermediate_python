from collections import Counter


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
    messy_tags = "python, Data , PYTHON,  files,python,data"
    result = normalize_and_count_tags(messy_tags)

    print("Normalized tags:")
    print(f"  Unique: {result['unique_tags']}")
    print(f"  Total unique: {result['total_unique']}")
    print(f"  Frequencies: {result['frequencies']}")

    # Verificaciones
    assert result['total_unique'] == 3, "Should have 3 unique tags"
    assert result['unique_tags'] == ["data", "files", "python"], "Should be sorted"
    assert result['frequencies']['python'] == 3, "Python appears 3 times"
