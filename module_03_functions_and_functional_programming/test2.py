# funciones con argumentos variables *args
def var_arguments(name: str, *args: int):
    print(f"estoy ejecutando la función para {name}")
    print(type(args))
    print(args)


var_arguments("harvey", 1, 2, 3)
