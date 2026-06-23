from dataclasses import dataclass


@dataclass
class Task:
    title: str
    completed: bool = False


class TaskRegistry:
    def __init__(self):
        self.tasks: list[Task] = []

    def add(self, task: Task) -> None:
        self.tasks.append(task)

    def pending_count(self) -> int:
        return sum(1 for task in self.tasks if not task.completed)


if __name__ == "__main__":
    registry = TaskRegistry()
    registry.add(Task("Notebook parity"))
    registry.add(Task("Exercise review", completed=True))
    print(registry.pending_count())
