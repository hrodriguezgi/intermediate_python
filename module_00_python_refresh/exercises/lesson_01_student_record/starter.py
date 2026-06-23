from __future__ import annotations


def build_student_records(students: list[dict]) -> list[dict]:
    """
    Process a list of student data and build normalized records.

    Each student dict has: name, age, email, track.
    - Normalize names (strip, title case).
    - Convert age from string to integer.
    - Return a list of dicts with normalized student data.
    """
    pass


if __name__ == "__main__":
    sample = [
        {"name": " ana garcia ", "age": "19", "email": "ana@example.com", "track": "backend"},
        {"name": " luis perez ", "age": "25", "email": "luis@example.com", "track": "data"},
        {"name": " sofia lopez ", "age": "21", "email": "sofia@example.com", "track": "backend"},
    ]
    result = build_student_records(sample)
    print(result)
