from functools import wraps


def retry(times: int):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            last_error = None
            for _ in range(times):
                try:
                    return function(*args, **kwargs)
                except ValueError as error:
                    last_error = error
            raise last_error

        return wrapper

    return decorator


if __name__ == "__main__":
    attempts = {"count": 0}

    @retry(3)
    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("not yet")
        return "ok"

    print(flaky())
