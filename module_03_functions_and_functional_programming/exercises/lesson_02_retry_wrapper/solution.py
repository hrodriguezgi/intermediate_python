import time
from functools import wraps


def retry(times: int):
    """
    Decorador que reintenta una función hasta `times` veces.

    Registra logs de cada intento y mide el tiempo total de ejecución.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            last_error = None

            for attempt in range(1, times + 1):
                try:
                    result = function(*args, **kwargs)
                    elapsed = time.perf_counter() - start
                    print(f" {function.__name__} completado en {elapsed:.2f}s")
                    return result
                except Exception as error:
                    last_error = error
                    args_str = ", ".join(repr(a) for a in args)
                    print(f"Intento {attempt}/{times}: {function.__name__}({args_str}) - " f"Falló ({type(error).__name__}: {error})")

            # Si llegamos aquí, todos los intentos fallaron
            raise last_error

        return wrapper

    return decorator


if __name__ == "__main__":
    # Caso de prueba: función que falla los primeros 2 intentos
    attempts = {"count": 0}

    @retry(times=3)
    def flaky_api_call():
        attempts["count"] += 1
        time.sleep(0.1)  # Simula I/O
        if attempts["count"] < 3:
            raise ValueError("API no disponible temporalmente")
        return {"status": "ok", "data": [1, 2, 3]}

    # Debe reintentar automáticamente y tener éxito en intento 3
    result = flaky_api_call()
    print(f"Resultado: {result}")

    # Caso 2: Falla permanente (agota intentos)
    print("\n--- Caso 2: Falla permanente ---")
    call_count = {"value": 0}

    @retry(times=2)
    def always_fails():
        call_count["value"] += 1
        raise RuntimeError("Conexión rechazada")

    try:
        always_fails()
    except RuntimeError as e:
        print(f"✗ Fallido después de todos los intentos: {e}")
