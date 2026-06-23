from __future__ import annotations


def process_enrollment_data(students: list[dict]) -> dict:
    """
    Process a list of student enrollment records.

    Each student dict has: name, age, email, track.
    - Normalize names (strip, title case).
    - Parse age as integer.
    - Validate: age >= 13, email is not empty.
    - Return a dict with:
        - "valid_students": list of dicts with processed student data
        - "rejected_students": list of dicts with name and reason
        - "total_valid": count of valid enrollments
        - "tracks": set of unique tracks from valid students
    """
    valid_students = []
    rejected_students = []
    tracks = set()

    for student in students:
        normalized_name = student["name"].strip().title()

        try:
            parsed_age = int(student["age"])
        except ValueError:
            rejected_students.append({
                "name": normalized_name,
                "reason": f"invalid age: {student['age']!r}",
            })
            continue

        if parsed_age < 13:
            rejected_students.append({
                "name": normalized_name,
                "reason": f"age {parsed_age} below minimum (13)",
            })
            continue

        if not student.get("email"):
            rejected_students.append({
                "name": normalized_name,
                "reason": "missing email",
            })
            continue

        valid_students.append({
            "name": normalized_name,
            "age": parsed_age,
            "email": student["email"],
            "track": student["track"],
        })
        tracks.add(student["track"])

    return {
        "valid_students": valid_students,
        "rejected_students": rejected_students,
        "total_valid": len(valid_students),
        "tracks": tracks,
    }


if __name__ == "__main__":
    sample = [
        {"name": " ana garcia ", "age": "19", "email": "ana@example.com", "track": "backend"},
        {"name": " luis perez ", "age": "25", "email": "", "track": "data"},
        {"name": " sofia lopez ", "age": "12", "email": "sofia@example.com", "track": "backend"},
        {"name": " carlos ", "age": "invalid", "email": "carlos@example.com", "track": "frontend"},
    ]
    result = process_enrollment_data(sample)
    print(result)
