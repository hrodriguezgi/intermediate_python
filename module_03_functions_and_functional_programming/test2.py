"""
Lección: *args (argumentos variables posicionales)

Permite aceptar cualquier cantidad de argumentos posicionales.
Los argumentos se reciben como TUPLA (tupla es inmutable).
"""

# Función que acepta cantidad variable de argumentos
def var_arguments(name: str, *args: int):
    """
    name: Nombre (obligatorio)
    *args: Cantidad variable de números (0 o más)

    Los argumentos variables se reciben como tupla.
    """
    print(f"estoy ejecutando la función para {name}")
    print(type(args))  # Muestra que es tupla
    print(args)


# Llamada con 3 argumentos después de name
var_arguments("harvey", 1, 2, 3)
