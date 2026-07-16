def var_kw_arguments(name: str, **kwargs: int):
    print(f"estoy ejecutando la función para {name}")
    print(type(kwargs))
    print(kwargs)


var_kw_arguments("harvey", math=1, science=2, geography=3)


def var_kw_arguments2(name: str, age: int = 20, **kwargs: int):
    print(f"estoy ejecutando la función para {name}")
    print(type(kwargs))
    print(kwargs)
    print(age)


var_kw_arguments2("harvey", math=1, science=2, geography=3)
