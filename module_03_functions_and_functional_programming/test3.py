"""
Lección: **kwargs (argumentos variables llave-valor)

Permite aceptar cualquier cantidad de argumentos nombrados.
Los argumentos se reciben como DICCIONARIO.
"""


# Función que acepta cantidad variable de argumentos nombrados
def var_kw_arguments(name: str, **kwargs: int):
    """
    name: Nombre (obligatorio)
    **kwargs: Cantidad variable de pares llave-valor (0 o más)

    Los argumentos nombrados se reciben como diccionario.
    """
    print(f"estoy ejecutando la función para {name}")
    print(type(kwargs))  # Muestra que es diccionario
    print(kwargs)


# Llamada con argumentos nombrados: math=1, science=2, geography=3
var_kw_arguments("harvey", math=1, science=2, geography=3)


# Función combinando argumentos obligatorios, opcionales y **kwargs
def var_kw_arguments2(name: str, age: int = 20, **kwargs: int):
    """
    name: Obligatorio
    age: Opcional con valor por defecto 20
    **kwargs: Cantidad variable de argumentos nombrados

    Orden: obligatorios -> opcionales -> **kwargs
    """
    print(f"estoy ejecutando la función para {name}")
    print(type(kwargs))  # Diccionario
    print(kwargs)
    print(age)


# Llamada: age usa valor por defecto, se pasan argumentos adicionales
var_kw_arguments2("harvey", math=1, science=2, geography=3)
