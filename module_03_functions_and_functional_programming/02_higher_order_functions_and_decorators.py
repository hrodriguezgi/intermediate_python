# %% [markdown]
# # 02. Higher-order functions y decoradores
#
# ## Objetivos
#
# - Pasar funciones como argumentos.
# - Reutilizar comportamientos transversales.

# %%
from functools import wraps

numbers = [5, 12, 18, 21]

# %% [markdown]
# ## `map` y `filter`

# %%
squared = list(map(lambda value: value * value, numbers))
large_values = list(filter(lambda value: value >= 15, numbers))

print(squared)
print(large_values)

# %% [markdown]
# ## Funciones de orden superior


# %%
def apply_pipeline(values: list[int], *operations) -> list[int]:
    result = values
    for operation in operations:
        result = operation(result)
    return result


def keep_even(values: list[int]) -> list[int]:
    return [value for value in values if value % 2 == 0]


def double(values: list[int]) -> list[int]:
    return [value * 2 for value in values]


print(apply_pipeline(numbers, keep_even, double))

# %% [markdown]
# ## Decoradores


# %%
def traced(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"calling {function.__name__} with args={args}, kwargs={kwargs}")
        result = function(*args, **kwargs)
        print(f"returned {result}")
        return result

    return wrapper


@traced
def compute_discount(total: float, rate: float) -> float:
    return round(total * (1 - rate), 2)


compute_discount(250, 0.15)

# %% [markdown]
# ## Resumen
#
# - Una función puede ser un dato más dentro del programa.
# - Los decoradores permiten encapsular trazabilidad y validación.
