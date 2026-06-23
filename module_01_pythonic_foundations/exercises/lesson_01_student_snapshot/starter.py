def build_student_snapshot(records: list[tuple[str, str, int]]) -> dict:
    tracks = set()
    total_years = 0

    for record in records:
        name, track, years = record
        tracks.add(track)
        total_years += years

    return {
        "total_students": len(records),
        "tracks": sorted(tracks),
        "experience_average": round(total_years / len(records), 2) if records else 0,
    }


if __name__ == "__main__":
    sample = [
        ("Ana", "backend", 2),
        ("Luis", "data", 4),
        ("Marta", "backend", 3),
    ]
    print(build_student_snapshot(sample))
