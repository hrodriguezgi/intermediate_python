import json


def build_event_digest(events: list[dict]) -> dict:
    """Part 1: Basic digest using comprehensions."""
    ok_events = [event for event in events if event["status"] == "ok"]
    return {
        "ok_count": len(ok_events),
        "users": sorted({event["user"] for event in ok_events}),
        "total_duration": sum(event["duration"] for event in ok_events),
    }


def build_event_digest_generator(events_iter) -> dict:
    """Part 2: Memory-efficient version using generators for large datasets.

    Key difference: Uses generator expressions (with parentheses)
    instead of list comprehensions (with brackets).
    """
    # Filter ok events lazily (not loading all in memory)
    ok_events_gen = (event for event in events_iter if event["status"] == "ok")

    # Need to materialize some data for the summary
    ok_events_list = list(ok_events_gen)  # Now we have them all

    return {
        "ok_count": len(ok_events_list),
        "users": sorted({event["user"] for event in ok_events_list}),
        "total_duration": sum(event["duration"] for event in ok_events_list),
    }


def build_event_digest_from_lines(lines: list[str]) -> dict:
    """Part 3: Parse events from JSON lines with validation using walrus operator."""
    result = {
        "ok_count": 0,
        "users": set(),
        "total_duration": 0,
        "invalid": [],
    }

    for line_idx, line in enumerate(lines):
        # Use walrus operator to validate while assigning
        if (parsed := _parse_json_safely(line)) is not None:
            event = parsed
            if event.get("status") == "ok":
                result["ok_count"] += 1
                result["users"].add(event.get("user"))
                result["total_duration"] += event.get("duration", 0)
        else:
            result["invalid"].append(line_idx)

    result["users"] = sorted(result["users"])
    return result


def _parse_json_safely(line: str) -> dict | None:
    """Helper function to parse JSON line, return None if invalid."""
    try:
        return json.loads(line)
    except (json.JSONDecodeError, ValueError):
        return None


if __name__ == "__main__":
    # Part 1: Basic example
    sample = [
        {"user": "ana", "duration": 30, "status": "ok"},
        {"user": "luis", "duration": 12, "status": "retry"},
        {"user": "ana", "duration": 15, "status": "ok"},
    ]
    print("Part 1 - Basic digest:")
    print(build_event_digest(sample))
    print()

    # Part 2: Large dataset (iterator)
    print("Part 2 - Generator-based digest:")
    events_iter = iter(sample)
    print(build_event_digest_generator(events_iter))
    print()

    # Part 3: Parse from JSON lines
    print("Part 3 - Digest from JSON lines:")
    log_lines = [
        '{"user": "ana", "duration": 30, "status": "ok"}',
        '{"user": "luis", "duration": 12, "status": "retry"}',
        'INVALID_JSON',
        '{"user": "marta", "duration": 48, "status": "ok"}',
    ]
    result = build_event_digest_from_lines(log_lines)
    print(result)
