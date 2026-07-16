# funciones con argumentos obligatorios
def say_hello(name: str, lastname: str) -> str:
    print("estoy ejecutando la función")
    return f"hola {name.capitalize()} {lastname.capitalize()}"


# argumentos enviados por posición
var = say_hello("harvey", "rodriguez")
print(var)

# argumentos enviados por asignación
var2 = say_hello(lastname="GOMEZ", name="SANDRA")
print(var2)


# funciones con argumentos obligatorios, variables y opcionales
def say_hello2(name: str, *subjects: str, age: int = 20) -> str:
    print("estoy ejecutando la función")
    return f"hola {name.capitalize()} las materias inscritas son: {subjects}, la edad es {age}"


# los opcionales deben ir despues de los "variables" y nombrados o por asignación
var3 = say_hello2("harvey", "math", "spain", "science", age=30)
print(var3)
