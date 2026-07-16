"""
Lección: Argumentos en funciones

Tipos:
1. Argumentos obligatorios posicionales
2. Argumentos por nombre (keyword arguments)
3. Argumentos variables (*args)
4. Argumentos opcionales con valor por defecto
"""

# Función con argumentos obligatorios
def say_hello(name: str, lastname: str) -> str:
    """Recibe nombre y apellido (ambos obligatorios)."""
    print("estoy ejecutando la función")
    return f"hola {name.capitalize()} {lastname.capitalize()}"


# Opción 1: Argumentos por posición (orden importa)
var = say_hello("harvey", "rodriguez")
print(var)

# Opción 2: Argumentos por nombre (keyword arguments)
# Ventaja: orden no importa, más legible
var2 = say_hello(lastname="GOMEZ", name="SANDRA")
print(var2)


# Función con argumentos: obligatorio + variables + opcional
def say_hello2(name: str, *subjects: str, age: int = 20) -> str:
    """
    name: Obligatorio
    *subjects: Cantidad variable de materias (0 o más)
    age: Opcional, tiene valor por defecto 20

    Orden de argumentos: obligatorios → *args → opcionales
    """
    print("estoy ejecutando la función")
    return f"hola {name.capitalize()} las materias inscritas son: {subjects}, la edad es {age}"


# Argumentos nombrados obligatorios DESPUÉS de *args deben pasarse por nombre
var3 = say_hello2("harvey", "math", "spain", "science", age=30)
print(var3)
