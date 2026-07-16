"""
Lección: Diferencia entre print() y return

- print(): Solo muestra en pantalla, no es reutilizable
- return: Devuelve valor que se puede reutilizar
"""

# Ejemplo 1: Usar print (output no es reutilizable)
def say_hello():
    """Imprime mensaje pero no devuelve nada."""
    print("estoy ejecutando la función")


# Invocamos función (output va a terminal)
say_hello()


# Ejemplo 2: Usar return (output es reutilizable)
def say_goodbye() -> str:
    """Devuelve mensaje que se puede usar después."""
    return "adiós mundo cruel"


# Guardamos valor devuelto en variable (reutilizable)
variable = say_goodbye()
# Usamos el valor en otro lugar
print(variable)
