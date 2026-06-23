from datetime import date, timedelta


def build_release_agenda(start_date: str, lesson_count: int) -> dict:
    current = date.fromisoformat(start_date)
    schedule = [
        (current + timedelta(days=7 * lesson_index)).isoformat()
        for lesson_index in range(lesson_count)
    ]
    return {
        "start_date": current.isoformat(),
        "lesson_count": lesson_count,
        "schedule": schedule,
    }


if __name__ == "__main__":
    print(build_release_agenda("2026-07-01", 4))
