from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate() -> None:
    modules = sorted(ROOT.glob("module_*"))
    assert modules, "No modules found"

    lesson_count = 0
    notebook_count = 0
    exercise_count = 0

    for module_dir in modules:
        readme = module_dir / "README.md"
        assert readme.exists(), f"Missing {readme}"

        lessons = sorted(module_dir.glob("[0-9][0-9]_*.py"))
        notebooks = sorted((module_dir / "notebooks").glob("*.ipynb"))
        exercise_readmes = sorted(module_dir.glob("exercises/*/README.md"))

        assert lessons, f"No lessons in {module_dir.name}"
        assert len(lessons) == len(notebooks), f"Notebook mismatch in {module_dir.name}"
        assert exercise_readmes, f"No exercises in {module_dir.name}"

        for notebook in notebooks:
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            assert payload["nbformat"] == 4, f"Invalid nbformat in {notebook}"
            assert payload["cells"], f"Notebook without cells: {notebook}"

        lesson_count += len(lessons)
        notebook_count += len(notebooks)
        exercise_count += len(exercise_readmes)

    print(
        f"Validated {len(modules)} modules, {lesson_count} lessons, "
        f"{notebook_count} notebooks, {exercise_count} exercises."
    )


if __name__ == "__main__":
    validate()
