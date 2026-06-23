def safe_parse_int(value, default: int = 0) -> int:
    """
    Convert a value to int safely, handling None, strings, and invalid input.

    - If value is None, return default.
    - If value is a string, try to convert to int.
    - If conversion fails, return default.
    """
    pass


def safe_parse_bool(value, default: bool = False) -> bool:
    """
    Convert a value to bool safely, handling multiple representations.

    - If value is None, return default.
    - If value is already bool, return it.
    - If value is a string:
      - "yes", "true", "1", "on" (case-insensitive) → True
      - Other strings → False
    - If value is a number:
      - 0 → False
      - Any other number → True
    """
    pass


def parse_user_record(user_data: dict) -> dict:
    """
    Parse and validate a user record with potentially messy data.

    Input dict may have inconsistent types:
    - id: required, should be int
    - name: required, should be string (strip, title case)
    - age: optional int (can be None, string, or empty list)
    - active: optional bool, default False
    - tags: optional list of strings (can be None, comma-separated string, or list)

    Raises ValueError if required fields (id, name) are None or empty.
    Returns a normalized dict with correct types.
    """
    pass


if __name__ == "__main__":
    # Test data with messy types
    users = [
        {
            "id": 1,
            "name": "  alice  ",
            "age": "30",
            "active": "yes",
            "tags": "python,data",
        },
        {
            "id": "2",
            "name": "bob",
            "age": None,
            "active": True,
            "tags": [],
        },
        {
            "id": 3,
            "name": " charlie ",
            "age": "invalid",
            "active": "no",
            "tags": None,
        },
    ]

    print("Parsing user records:")
    for user in users:
        try:
            parsed = parse_user_record(user)
            print(f"  ✓ {parsed}")
        except ValueError as e:
            print(f"  ✗ Error: {e}")
