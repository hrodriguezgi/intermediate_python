def build_student_snapshot(records: list[tuple[str, str, int]]) -> dict:
    """
    Construye un resumen estadístico de estudiantes a partir de registros de tuplas.

    Args:
        records: Lista de tuplas (nombre, track, años_experiencia)

    Returns:
        Diccionario con total_students, tracks ordenados, y experience_average
    """
    # TODO: Implementa la función aquí


if __name__ == "__main__":
    sample = [
        ("Ana", "backend", 2),
        ("Luis", "data", 4),
        ("Marta", "backend", 3),
    ]
    result = build_student_snapshot(sample)
    print(result)
