# %% [markdown]
# # 01. Clases, dataclasses y métodos especiales
#
# ## Objetivos
#
# - Modelar entidades simples con clases.
# - Reducir ruido con `@dataclass`.

# %%
from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    duration_minutes: int
    published: bool = False

    def publish(self) -> None:
        self.published = True


lesson = Lesson("Archivos con pathlib", 45)
print(lesson)
lesson.publish()
print(lesson)

# %% [markdown]
# ## Métodos especiales


# %%
class Cohort:
    def __init__(self, name: str, students: list[str]):
        self.name = name
        self.students = students

    def __len__(self) -> int:
        return len(self.students)

    def __repr__(self) -> str:
        return f"Cohort(name={self.name!r}, students={self.students!r})"


cohort = Cohort("Noche", ["Ana", "Luis", "Marta"])
print(cohort)
print(len(cohort))

# %% [markdown]
# ## Resumen
#
# - `dataclass` es excelente para modelos de datos.
# - Los métodos especiales mejoran la integración con Python.
