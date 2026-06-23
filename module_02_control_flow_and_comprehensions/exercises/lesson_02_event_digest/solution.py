def build_event_digest(events: list[dict]) -> dict:
    ok_events = [event for event in events if event["status"] == "ok"]
    return {
        "ok_count": len(ok_events),
        "users": sorted({event["user"] for event in ok_events}),
        "total_duration": sum(event["duration"] for event in ok_events),
    }


if __name__ == "__main__":
    sample = [
        {"user": "ana", "duration": 30, "status": "ok"},
        {"user": "luis", "duration": 12, "status": "retry"},
        {"user": "ana", "duration": 15, "status": "ok"},
    ]
    print(build_event_digest(sample))
