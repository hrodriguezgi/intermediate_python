from dataclasses import dataclass

# ============================================================================
# COMPARACIÓN: oop_1.py vs oop_2.py
# ============================================================================
# oop_1.py: Implementa __init__ manualmente + dunder methods explícitos
# oop_2.py: Usa @dataclass que genera __init__ y __repr__ automáticamente
# ============================================================================


@dataclass
class Student:
    """Un estudiante con nombre y email (usando @dataclass).

    @dataclass genera automáticamente:
    - __init__(self, name: str, email: str)
    - __repr__(self) -> string para debugging
    - __eq__(self, other) -> comparación con ==
    - __hash__() -> si frozen=True

    Reducción de código repetitivo: 15 líneas → 5 líneas.

    Demuestra:
    - Type hints para atributos (name, email)
    - Atributos se convierten en parámetros de __init__
    - Dunder methods generados automáticamente
    - Métodos estáticos (@staticmethod)
    - Métodos de clase (@classmethod)
    """

    # ATRIBUTOS DE INSTANCIA (se convierten en parámetros de __init__)
    name: str
    email: str

    def print_info(self) -> None:
        """Método regular: imprime información del estudiante."""
        print(f"{self.name} ({self.email})")

    @staticmethod
    def print_saludo():
        """Método estático: no accede a instancia ni clase.

        Se llama con: Student.print_saludo() o instance.print_saludo()
        Útil para utilidades relacionadas a la clase.
        """
        print("Bienvenido al nuevo año escolar")

    @classmethod
    def otro_email(cls, email_alterno="otro@email.com"):
        """Método de clase: accede a atributos de clase.

        Se llama con: Student.otro_email("new@email.com")
        Modifica atributos compartidos por todas las instancias.
        """
        cls.email_alterno = email_alterno


# ============================================================================
# DEMOSTRACIÓN: Creación de instancias
# ============================================================================
print("--- Creación de instancias con @dataclass ---")
# @dataclass genera automáticamente __init__, así que funciona igual
estudiante_1 = Student("Pepito", "pepito@email.com")
estudiante_2 = Student("Fulanito", "fulanito@email.com")
print()

# ============================================================================
# MÉTODOS REGULARES: Operan en la instancia (self)
# ============================================================================
print("--- Métodos regulares ---")
estudiante_1.print_info()
estudiante_2.print_info()
print()

# ============================================================================
# MÉTODOS ESTÁTICOS
# ============================================================================
print("--- Métodos estáticos ---")
estudiante_2.print_saludo()
print()

# ============================================================================
# DUNDER METHOD GENERADO: __repr__ (automático con @dataclass)
# ============================================================================
print("--- Dunder method __repr__ (generado automáticamente) ---")
print(estudiante_2)  # @dataclass genera __repr__ automáticamente
# Output: Student(name='Fulanito', email='fulanito@email.com')
