import copy


def create_student_backup(students: list[dict]) -> list[dict]:
    """
    Crea una copia profunda de registros de estudiantes para backup seguro.

    Args:
        students: Lista de diccionarios con datos de estudiantes (pueden tener datos anidados)

    Returns:
        Una copia profunda e independiente de los registros originales
    """
    # TODO: Implementa la función aquí


if __name__ == "__main__":
    students = [
        {
            "id": 1,
            "name": "Ana",
            "metadata": {"track": "backend", "years": 2}
        },
        {
            "id": 2,
            "name": "Luis",
            "metadata": {"track": "data", "years": 4}
        },
    ]

    backup = create_student_backup(students)

    # Modifica el backup
    backup[0]["name"] = "Anna"
    backup[0]["metadata"]["years"] = 5

    # Verifica que el original está intacto
    print("Original students[0]:", students[0])
    print("Backup students[0]:", backup[0])
    print("Are they independent?", students[0] != backup[0])
