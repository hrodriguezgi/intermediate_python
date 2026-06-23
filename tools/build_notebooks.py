from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_percent_script(script_path: Path) -> dict:
    lines = script_path.read_text(encoding="utf-8").splitlines()
    cells: list[tuple[str, list[str]]] = []
    current_type: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_type, current_lines
        if current_type is None:
            return
        while current_lines and current_lines[-1] == "":
            current_lines.pop()
        cells.append((current_type, current_lines[:]))
        current_type = None
        current_lines = []

    for line in lines:
        if line.startswith("# %%"):
            flush()
            current_type = "markdown" if "[markdown]" in line else "code"
            continue
        if current_type is None:
            current_type = "code"
        current_lines.append(line)

    flush()

    notebook_cells = []
    for cell_type, cell_lines in cells:
        if cell_type == "markdown":
            markdown_lines = []
            for raw_line in cell_lines:
                if raw_line.startswith("# "):
                    markdown_lines.append(raw_line[2:])
                elif raw_line == "#":
                    markdown_lines.append("")
                elif raw_line.startswith("#"):
                    markdown_lines.append(raw_line[1:])
                else:
                    markdown_lines.append(raw_line)
            source = "\n".join(markdown_lines).strip("\n")
        else:
            source = "\n".join(cell_lines).rstrip()

        if not source:
            continue

        cell = {
            "cell_type": cell_type,
            "metadata": {},
            "source": [line + "\n" for line in source.split("\n")],
        }
        if cell_type == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

        notebook_cells.append(cell)

    return {
        "cells": notebook_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.12",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build_notebooks() -> int:
    count = 0
    for module_dir in sorted(ROOT.glob("module_*")):
        notebooks_dir = module_dir / "notebooks"
        notebooks_dir.mkdir(exist_ok=True)
        for script_path in sorted(module_dir.glob("[0-9][0-9]_*.py")):
            notebook = parse_percent_script(script_path)
            notebook_path = notebooks_dir / f"{script_path.stem}.ipynb"
            notebook_path.write_text(
                json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            count += 1
    return count


if __name__ == "__main__":
    built = build_notebooks()
    print(f"Built {built} notebook(s).")
