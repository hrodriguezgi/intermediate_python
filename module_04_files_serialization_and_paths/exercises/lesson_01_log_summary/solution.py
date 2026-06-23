from pathlib import Path


def summarize_log(path: Path) -> dict:
    summary = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    for line in path.read_text(encoding="utf-8").splitlines():
        for level in summary:
            if line.startswith(level):
                summary[level] += 1
    return summary


if __name__ == "__main__":
    log_path = Path(__file__).resolve().parents[2] / "data" / "sample_log.txt"
    print(summarize_log(log_path))
