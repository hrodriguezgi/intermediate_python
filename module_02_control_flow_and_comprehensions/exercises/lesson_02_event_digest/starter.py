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
    """Part 2: Memory-efficient version using generators for large datasets."""
    # TODO: Implement using generator expressions instead of list comprehensions
    # Process events without loading everything in memory
    # Return the same structure as build_event_digest
    pass


def build_event_digest_from_lines(lines: list[str]) -> dict:
    """Part 3: Parse events from JSON lines and validate with walrus operator."""
    # TODO: Implement using walrus operator for validation
    # - Read and parse JSON line by line
    # - Validate using walrus operator (line := ...)
    # - Handle parsing errors gracefully
    # Return dict with same structure + 'invalid' field for error indices
    pass


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
    # Simulating a large dataset with an iterator
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
    print(build_event_digest_from_lines(log_lines))
