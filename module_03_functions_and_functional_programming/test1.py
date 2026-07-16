def say_hello(name: str, lastname: str) -> str:
    print("estoy ejecutando la función")
    return f"hola {name.capitalize()} {lastname.capitalize()}"


var = say_hello("harvey", "rodriguez")
print(var)

var2 = say_hello(lastname="GOMEZ", name="SANDRA")
print(var2)


def say_hello2(name: str, *subjects: str, age: int = 20) -> str:
    print("estoy ejecutando la función")
    return f"hola {name.capitalize()} las materias inscritas son: {subjects}, la edad es {age}"


var3 = say_hello2("harvey", "math", "spain", "science", age=30)
print(var3)
