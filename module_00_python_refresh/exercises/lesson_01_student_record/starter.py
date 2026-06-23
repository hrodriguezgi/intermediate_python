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
    pass


if __name__ == "__main__":
    sample = [
        {"name": " ana garcia ", "age": "19", "email": "ana@example.com", "track": "backend"},
        {"name": " luis perez ", "age": "25", "email": "", "track": "data"},
        {"name": " sofia lopez ", "age": "12", "email": "sofia@example.com", "track": "backend"},
        {"name": " carlos ", "age": "invalid", "email": "carlos@example.com", "track": "frontend"},
    ]
    result = process_enrollment_data(sample)
    print(result)
e