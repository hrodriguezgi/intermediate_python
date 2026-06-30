from datetime import date, timedelta


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


if __name__ == "__main__":
    result = build_release_agenda("2026-07-01", 4)
    print(result)
