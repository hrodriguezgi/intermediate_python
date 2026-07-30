class Student:
    """Un estudiante con nombre y email.

    Demuestra:
    - Atributos de instancia (__init__)
    - Atributos de clase (compartidos entre instancias)
    - Dunder methods (__str__, __repr__, __eq__)
    - Métodos estáticos (@staticmethod)
    - Métodos de clase (@classmethod)
    """

    # ATRIBUTO DE CLASE: Compartido entre todas las instancias
    # Se accede vía ClassName.attribute o instance.attribute
    EMAIL_ALTERNO = "yaper@email.com"

    def __init__(self, name: str, email: str) -> None:
        """Constructor: inicializa atributos de instancia.

        Se llama automáticamente al crear un objeto: Student("Ana", "ana@ex.com")

        Args:
            name: Nombre del estudiante
            email: Email del estudiante
        """
        # ATRIBUTOS DE INSTANCIA: Únicos para cada objeto
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Representa el objeto como string legible para humanos.

        Se llama con: str(obj) o print(obj)
        Ideal para mensajes amigables al usuario.
        """
        return f"Student(name='{self.name}', email='{self.email}')"

    def __repr__(self) -> str:
        """Representa el objeto para debugging.

        Se llama con: repr(obj) o en el REPL sin print()
        Ideal para desarrolladores: debe mostrar cómo reconstruir el objeto.
        """
        return f"Student(name='{self.name}', email='{self.email}')"

    def print_info(self) -> None:
        """Método regular: imprime información del estudiante."""
        print(f"{self.name} ({self.email})")

    def __eq__(self, other) -> bool:
        """Permite comparación con ==.

        Se llama con: obj1 == obj2
        Retorna True si tienen mismo nombre y email.
        """
        print("Validando igualdad")
        return (self.name == other.name) and (self.email == other.email)

    @staticmethod
    def print_saludo():
        """Método estático: no accede a instancia ni clase.

        Se llama con: Student.print_saludo() o instance.print_saludo()
        No recibe self ni cls, es una función dentro de la clase.
        Útil para utilidades relacionadas a la clase.
        """
        print("Bienvenido al nuevo año escolar")

    @classmethod
    def otro_email(cls, email_alterno):
        """Método de clase: accede a atributos de clase.

        Se llama con: Student.otro_email("new@email.com")
        Recibe cls (la clase) en lugar de self (la instancia).
        Modifica atributos compartidos por TODAS las instancias.
        """
        cls.EMAIL_ALTERNO = email_alterno


# ============================================================================
# DEMOSTRACIÓN: Creación de instancias e interacción
# ============================================================================

# Crear dos instancias (cada una con sus propios atributos)
estudiante_1 = Student("Pepito", "pepito@email.com")
estudiante_2 = Student("Fulanito", "pepito@email.com")
print()

# ============================================================================
# MÉTODOS REGULARES: Operan en la instancia (self)
# ============================================================================
print("--- Métodos regulares ---")
estudiante_1.print_info()  # Llama al método en estudiante_1
estudiante_2.print_info()  # Llama al método en estudiante_2
print()

# ============================================================================
# MÉTODOS ESTÁTICOS: No acceden a instancia ni clase
# ============================================================================
print("--- Métodos estáticos ---")
estudiante_2.print_saludo()  # Se puede llamar desde instancia o clase
print()

# ============================================================================
# DUNDER METHODS: Python los llama automáticamente
# ============================================================================
print("--- Dunder methods: __str__ y __repr__ ---")
print(estudiante_2)  # Llama a __str__ (para usuarios)
print(repr(estudiante_1))  # Llama a __repr__ (para desarrolladores)
print()

# ============================================================================
# DUNDER METHOD: __eq__ para comparación con ==
# ============================================================================
print("--- Dunder method: __eq__ para comparación ---")
print(estudiante_2 == estudiante_1)  # Llama a __eq__, retorna False
print()

# ============================================================================
# ATRIBUTOS DE CLASE: Compartidos entre todas las instancias
# ============================================================================
print("--- Atributos de clase (antes de cambiar) ---")
print(f"estudiante_1.EMAIL_ALTERNO: {estudiante_1.EMAIL_ALTERNO}")
print(f"estudiante_2.EMAIL_ALTERNO: {estudiante_2.EMAIL_ALTERNO}")
print()

# ============================================================================
# MÉTODOS DE CLASE: Modifican atributos de clase
# ============================================================================
print("--- Método de clase: otro_email() ---")
print("Llamando: Student.otro_email('sutanito@email.com')")
Student.otro_email("sutanito@email.com")  # Modifica EMAIL_ALTERNO para TODAS las instancias

# Ambas instancias ahora ven el nuevo valor
print(f"estudiante_1.EMAIL_ALTERNO: {estudiante_1.EMAIL_ALTERNO}")
print(f"estudiante_2.EMAIL_ALTERNO: {estudiante_2.EMAIL_ALTERNO}")
print()
