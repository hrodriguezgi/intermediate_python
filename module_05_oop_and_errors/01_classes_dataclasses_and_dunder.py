# %% [markdown]
# # 01. Clases, dataclasses y métodos especiales
#
# ## Objetivos
#
# - Modelar entidades simples con clases.
# - Reducir ruido con `@dataclass`.

# %%
from abc import ABC, abstractmethod
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
# ## Herencia vs Composición
#
# ### El Problema: Herencia para todo
#
# La herencia es tentadora, pero causa problemas en objetos de datos cuando necesitas
# combinar comportamientos. En ingeniería de datos, composición es casi siempre mejor.

# %%
# Anti-patrón: herencia profunda
class DataSource(ABC):
    @abstractmethod
    def read(self) -> dict:
        pass


class CSVSource(DataSource):
    def __init__(self, path: str):
        self.path = path

    def read(self) -> dict:
        # Simular lectura de CSV
        return {"rows": 1000, "columns": 10}


class JSONSource(DataSource):
    def __init__(self, url: str):
        self.url = url

    def read(self) -> dict:
        # Simular lectura de JSON
        return {"items": 500}


# Si necesitas agregar caché, ahora tenemos un problema:
# ¿Hereda CSVSource de DataSource o de Cache?
# Múltiple herencia se complica rápido.

# %% [markdown]
# ### La Solución: Composición
#
# Componemos objetos simples en lugar de heredar. Mucho más flexible.

# %%
class Cache:
    def __init__(self):
        self._data = {}

    def has(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str) -> dict:
        return self._data[key]

    def set(self, key: str, value: dict) -> None:
        self._data[key] = value


class DataReader:
    """Lee datos de una fuente con caché opcional."""

    def __init__(self, source: DataSource, cache: Cache | None = None):
        self.source = source
        self.cache = cache

    def read(self, cache_key: str | None = None) -> dict:
        # Intentar desde caché primero
        if cache_key and self.cache and self.cache.has(cache_key):
            print(f"✓ Desde caché: {cache_key}")
            return self.cache.get(cache_key)

        # Leer de la fuente
        print("→ Leyendo desde fuente...")
        data = self.source.read()

        # Guardar en caché si es posible
        if cache_key and self.cache:
            self.cache.set(cache_key, data)

        return data


# Uso: flexible y sin múltiple herencia
csv_source = CSVSource("data.csv")
cache = Cache()
reader = DataReader(csv_source, cache)

print(reader.read("csv_data"))  # Lee de fuente
print(reader.read("csv_data"))  # Desde caché

# Ahora es trivial agregar otra fuente o usar sin caché
json_source = JSONSource("https://api.example.com/data")
reader_no_cache = DataReader(json_source)
print(reader_no_cache.read())

# %% [markdown]
# ### Cuándo Usar Cada Uno
#
# **Herencia:** Solo para relaciones "es un" genuinas (Animal -> Perro)
# **Composición:** Para combinar comportamientos (Object + Logger, DataSource + Cache)
#
# En ingeniería de datos: usa composición el 95% del tiempo.

# %% [markdown]
# ## Resumen
#
# - `dataclass` es excelente para modelos de datos.
# - Los métodos especiales mejoran la integración con Python.
# - **Prefer composición sobre herencia para objetos de datos.**
