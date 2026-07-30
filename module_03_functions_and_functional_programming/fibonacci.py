from functools import lru_cache


# Decorador HOF que guarda los resultados de las funciones
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Imprime los primeros 10 números
resultado = [fibonacci(i) for i in range(10)]
print(resultado)
