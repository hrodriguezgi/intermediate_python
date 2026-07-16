import time
from functools import wraps


def retry(times: int):
    """
    Decorador que reintenta una función hasta `times` veces.

    Debe:
    1. Capturar excepciones y reintentar
    2. Registrar logs de cada intento
    3. Medir tiempo total de ejecución
    4. Relanzar la última excepción si todos fallan
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Tu código aquí
            # Pista:
            # - Usa un bucle para reintentar
            # - Registra: f"Intento {attempt}/{times}: {function.__name__}(...) - "
            # - Mide tiempo con time.perf_counter()
            # - Si es exitoso, imprime: f" Completado en {elapsed:.2f}s"
            pass

        return wrapper

    return decorator


if __name__ == "__main__":
    # Caso de prueba: función que falla los primeros 2 intentos
    attempts = {"count": 0}

    @retry(times=3)
    def flaky_api_call():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("API no disponible temporalmente")
        return {"status": "ok", "data": [1, 2, 3]}

    # Debe reintentar automáticamente y tener éxito en intento 3
    result = flaky_api_call()
    print(f"Resultado: {result}")
