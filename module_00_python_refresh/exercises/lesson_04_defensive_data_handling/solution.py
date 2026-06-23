def safe_parse_int(value, default: int = 0) -> int:
    """
    Convert a value to int safely, handling None, strings, and invalid input.

    - If value is None, return default.
    - If value is a string, try to convert to int.
    - If conversion fails, return default.
    """
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


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
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("yes", "true", "1", "on")
    # For numbers
    return bool(value)


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
    # Validate required fields
    if user_data.get("id") is None:
        raise ValueError("id is required")

    name = user_data.get("name")
    if name is None or (isinstance(name, str) and not name.strip()):
        raise ValueError("name is required")

    # Parse id (can be int or string)
    record_id = safe_parse_int(user_data["id"])
    if record_id == 0 and user_data["id"] != 0 and user_data["id"] != "0":
        raise ValueError(f"id must be a valid integer, got {user_data['id']}")

    # Parse name (strip and title case)
    parsed_name = name.strip().title() if isinstance(name, str) else str(name)

    # Parse age (optional, can be None or various formats)
    age_value = user_data.get("age")
    parsed_age = safe_parse_int(age_value) if age_value not in (None, [], "") else None

    # Parse active (optional, default False)
    parsed_active = safe_parse_bool(user_data.get("active"), default=False)

    # Parse tags (can be None, string with commas, or list)
    tags_value = user_data.get("tags")
    if tags_value is None or tags_value == []:
        parsed_tags = []
    elif isinstance(tags_value, str):
        parsed_tags = [tag.strip() for tag in tags_value.split(",") if tag.strip()]
    elif isinstance(tags_value, list):
        parsed_tags = tags_value
    else:
        parsed_tags = []

    return {
        "id": record_id,
        "name": parsed_name,
        "age": parsed_age,
        "active": parsed_active,
        "tags": parsed_tags,
    }


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
