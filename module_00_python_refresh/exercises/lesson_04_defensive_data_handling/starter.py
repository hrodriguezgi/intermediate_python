def safe_parse_int(value, default: int = 0) -> int:
    """
    Convert a value to int safely, handling None, strings, and invalid input.

    - If value is None, return default.
    - If value is a string, try to convert to int.
    - If conversion fails, return default.
    """
    # if value is None:
    #    return default
    try:
        return int(value)
    except ValueError:
        return default
    except TypeError:
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

    if isinstance(value, str) and value.strip().lower() in ("yes", "true", "1", "on"):
        return True
    else:
        return False

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
    input_id = user_data.get("id")
    if input_id is None or str(input_id).strip() == "":
        raise ValueError("id es requerido, favor validar los datos de entrada")

    input_name = user_data.get("name")
    if input_name is None or str(input_name).strip() == "":
        raise ValueError("name es requerido, favor validar el valor de entrada")

    output_id = safe_parse_int(input_id)

    output_name = input_name.strip().title()

    output_age = safe_parse_int(user_data.get("age"))

    output_active = safe_parse_bool(user_data.get("active"))

    input_tags = user_data.get("tags")
    if input_tags is None:
        output_tags = []
    elif isinstance(input_tags, str):
        output_tags = input_tags.split(",")
    elif isinstance(input_tags, list):
        output_tags = input_tags
    else:
        output_tags = []

    return {"id": output_id, "name": output_name, "age": output_age, "active": output_active, "tags": output_tags}


if __name__ == "__main__":
    # Test data with messy types
    users = [
        {
            "id": 1,
            "name": "",  # "  alice  ",
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
