# %% [markdown]
# # 01. Clases, dataclasses y métodos especiales
#
# ## Objetivos
#
# - Entender clases: el blueprint para objetos
# - Usar atributos (state) y métodos (behavior)
# - Comprender `__init__` constructor
# - Reducir código repetitivo con `@dataclass`

# %%
from abc import ABC, abstractmethod
from dataclasses import dataclass

# %% [markdown]
# ## ¿Por qué clases?
#
# Las clases agrupan datos relacionados (atributos) con funciones que operan
# en esos datos (métodos). Esto es **encapsulación** - bundling data with code.

# %% [markdown]
# ## Clases Básicas: Atributos y Métodos

# %%
# Un ejemplo simple sin clases:
student_name = "Ana"
student_email = "ana@example.com"


def print_student_info(name, email):
    print(f"{name} ({email})")


print_student_info(student_name, student_email)

# %% [markdown]
# ### Con una clase: agrupamos datos y comportamiento


# %%
class Student:
    """Un estudiante con nombre y email."""

    def set_info(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    def print_info(self) -> None:
        print(f"{self.name} ({self.email})")


student = Student()
student.set_info("Ana", "ana@example.com")
student.print_info()

# %% [markdown]
# ### El Constructor (`__init__`)
#
# El constructor inicializa atributos cuando se crea el objeto.
# Se llama automáticamente al instanciar la clase.


# %%
class Student2:
    """Un estudiante con nombre y email."""

    def __init__(self, name: str, email: str) -> None:
        """Inicializa el estudiante con nombre y email."""
        self.name = name
        self.email = email

    def print_info(self) -> None:
        print(f"{self.name} ({self.email})")


# Ahora los datos se inicializan automáticamente
student1 = Student("Ana", "ana@example.com")
student2 = Student("Luis", "luis@example.com")

student1.print_info()
student2.print_info()

# %% [markdown]
# ## `@dataclass`: Simplificando el Constructor
#
# Escribir `__init__` es repetitivo cuando solo inicializas atributos.
# El decorador `@dataclass` genera el `__init__` automáticamente.


@dataclass
class Lesson:
    """Una lección con título y duración."""

    title: str
    duration_minutes: int
    published: bool = False

    def publish(self) -> None:
        self.published = True


# `@dataclass` genera automáticamente:
# def __init__(self, title: str, duration_minutes: int, published: bool = False)
lesson = Lesson("Archivos con pathlib", 45)
print(lesson)
lesson.publish()
print(lesson)

# %% [markdown]
# ## Métodos Especiales (Dunder Methods)
#
# Python llama automáticamente a ciertos métodos especiales en situaciones específicas.
# Se reconocen por el prefijo y sufijo `__` (dunder = double underscore).


# %%
class Cohort:
    """Una cohorte de estudiantes."""

    def __init__(self, name: str, students: list[str]) -> None:
        self.name = name
        self.students = students

    def __repr__(self) -> str:
        """Representa el objeto como string (para debugging)."""
        return f"Cohort(name={self.name!r}, students={self.students!r})"

    def __len__(self) -> int:
        """Permite usar len(cohort)."""
        return len(self.students)


cohort = Cohort("Noche", ["Ana", "Luis", "Marta"])
print(cohort)  # Llama a __repr__
print(len(cohort))  # Llama a __len__

# %% [markdown]
# ### Métodos Especiales Comunes
#
# | Método | Cuándo se llama | Ejemplo |
# |--------|-----------------|---------|
# | `__init__` | Al crear un objeto | `obj = MyClass()` |
# | `__repr__` | Al hacer print() o en el REPL | `print(obj)` |
# | `__len__` | Al usar len() | `len(obj)` |
# | `__str__` | Cuando necesitas string legible | `str(obj)` |
# | `__eq__` | Al comparar con == | `obj1 == obj2` |
#
# Con `@dataclass`, se generan automáticamente `__init__` y `__repr__`:


# %%
@dataclass
class SimpleLesson:
    """@dataclass genera __init__ y __repr__ automáticamente."""

    title: str
    duration: int


lesson = SimpleLesson("OOP", 90)
print(lesson)  # __repr__ automático
# SimpleLesson(title='OOP', duration=90)

# %% [markdown]
# ## Herencia vs Composición
#
# ### El Problema: Herencia profunda
#
# La herencia funciona bien para relaciones "es un", pero cuando necesitas combinar
# comportamientos de múltiples clases, la herencia profunda se vuelve problemática.


# %%
# Anti-patrón: herencia profunda
class DataSource(ABC):
    def __init__(self, name):
        self.name = name

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
    """Lee datos de una fuente, opcionalmente con caché."""

    def __init__(self, source: DataSource, cache: Cache | None = None) -> None:
        self.source = source
        self.cache = cache

    def read(self, cache_key: str | None = None) -> dict:
        # Intentar desde caché primero
        if cache_key and self.cache and self.cache.has(cache_key):
            print(f" Desde caché: {cache_key}")
            return self.cache.get(cache_key)

        # Leer de la fuente
        print(" Leyendo desde fuente...")
        data = self.source.read()

        # Guardar en caché si es posible
        if cache_key and self.cache:
            self.cache.set(cache_key, data)

        return data


# La composición es flexible: mismo código funciona con cualquier DataSource
csv_source = CSVSource("data.csv")
cache = Cache()
reader = DataReader(csv_source, cache)

# %%

# Hacemos un primer llamado del método read
print(reader.read("csv_data"))  # Lee de fuente

# %%

# Hacemos un segundo llamado del método read
print(reader.read("csv_data"))  # Desde caché

# %%

# Funciona con otras fuentes sin cambiar DataReader
json_source = JSONSource("https://api.example.com/data")
reader_json = DataReader(json_source, cache)
print(reader_json.read("api_data"))

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
# - **Clases** agrupan datos (atributos) y funciones (métodos) - encapsulación
# - **`__init__`** inicializa atributos cuando se crea el objeto
# - **`@dataclass`** genera automáticamente `__init__` y `__repr__` para reducir código
# - **Métodos especiales** (`__repr__`, `__len__`, etc.) integran objetos con Python
# - **Composición** es más flexible que herencia para combinar comportamientos
