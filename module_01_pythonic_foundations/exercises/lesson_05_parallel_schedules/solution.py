def build_lesson_schedule(
    topics: list[str],
    durations: list[int],
    instructors: list[str],
) -> list[dict]:
    """
    Construye un calendario de lecciones a partir de datos paralelos.

    Args:
        topics: Lista de nombres de temas
        durations: Lista de duraciones en minutos
        instructors: Lista de instructores asignados

    Returns:
        Lista de diccionarios con numero, topic, minutes, e instructor
    """
    return [
        {
            "number": number,
            "topic": topic,
            "minutes": minutes,
            "instructor": instructor,
        }
        for number, (topic, minutes, instructor) in enumerate(zip(topics, durations, instructors), start=1)
    ]


if __name__ == "__main__":
    topics = ["Variables", "Funciones", "SQLite"]
    durations = [45, 60, 90]
    instructors = ["Ana", "Luis", "Marta"]

    schedule = build_lesson_schedule(topics, durations, instructors)

    print("Lesson Schedule:")
    for lesson in schedule:
        print(f"  Lesson {lesson['number']}: {lesson['topic']} " f"({lesson['minutes']} min, instructor: {lesson['instructor']})")

    # Verificaciones
    assert len(schedule) == 3, "Should have 3 lessons"
    assert schedule[0]["number"] == 1, "First lesson should be number 1"
    assert schedule[1]["topic"] == "Funciones", "Second topic should be Funciones"
    assert schedule[2]["instructor"] == "Marta", "Third instructor should be Marta"
    print(" All assertions passed!")
