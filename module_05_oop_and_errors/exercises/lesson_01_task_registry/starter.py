from dataclasses import dataclass


@dataclass
class Task:
    """Representa una tarea individual."""
    title: str
    completed: bool = False

    def __repr__(self) -> str:
        return f"Task('{self.title}', completed={self.completed})"


class TaskRegistry:
    """Gestiona una colección de tareas."""

    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add(self, task: Task) -> None:
        """Agrega una tarea al registro."""
        self.tasks.append(task)

    def pending_count(self) -> int:
        """Retorna cantidad de tareas incompletas."""
        # TODO: Implementa esto
        pass

    def completed_count(self) -> int:
        """Retorna cantidad de tareas completadas."""
        # TODO: Implementa esto
        pass

    def __len__(self) -> int:
        """Permite usar len(registry) para obtener total de tareas."""
        # TODO: Implementa esto (retorna total de tareas)
        pass

    def __repr__(self) -> str:
        """Representa el registro de tareas."""
        # TODO: Implementa esto
        # Formato esperado: TaskRegistry(N tasks, M pending)
        pass


if __name__ == "__main__":
    registry = TaskRegistry()
    registry.add(Task("Comprar leche"))
    registry.add(Task("Estudiar OOP", completed=True))
    registry.add(Task("Hacer ejercicio"))

    print(f"Total: {len(registry)}")
    print(f"Pendientes: {registry.pending_count()}")
    print(f"Completadas: {registry.completed_count()}")
    print(f"Registry: {registry}")
