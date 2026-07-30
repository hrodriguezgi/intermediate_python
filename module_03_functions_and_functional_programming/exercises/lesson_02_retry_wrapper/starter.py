import time
from functools import wraps


def retry(times: int):
    """
    Decorador que reintenta una función hasta `times` veces.

    Debe:
    1. Capturar excepciones y reintentar
    2. Registrar logs de cada intento
    3. Medir tiempo total de ejecución OK
    4. Relanzar la última excepción si todos fallan
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()

            for retry in range(1, times + 1):
                try:
                    result = function(*args, **kwargs)
                    total_time = time.perf_counter() - start_time
                    print(f"La función {function.__name__} se ejecutó correctamente en el reintento {retry} y la duración fue de: {total_time}")
                    return result
                except Exception as e:
                    print(f"La función {function.__name__} tuvo un fallo en el reintento {retry}: {str(e)}")

        return wrapper

    return decorator


def retries(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        for retry in range(1, 4):
            try:
                result = function(*args, **kwargs)
                total_time = time.perf_counter() - start_time
                print(f"La función {function.__name__} se ejecutó correctamente en el reintento {retry} y la duración fue de: {total_time}")
                return result
            except Exception as e:
                print(f"La función {function.__name__} tuvo un fallo en el reintento {retry}: {str(e)}")

    return wrapper


if __name__ == "__main__":
    # Caso de prueba: función que falla los primeros 2 intentos
    attempts = {"count": 0}

    @retry(times=3)
    # @retries
    def flaky_api_call():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("API no disponible temporalmente")
        return {"status": "ok", "data": [1, 2, 3]}, True

    # Debe reintentar automáticamente y tener éxito en intento 3
    # final_result = flaky_api_call()
    dict_result, bool_result = flaky_api_call()
    print(f"Resultado: {dict_result}\n{bool_result}")
