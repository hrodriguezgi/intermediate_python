"""
Lección: map() y filter()

Concepto:
- map(): Aplica función a cada elemento (transformación)
- filter(): Selecciona elementos que cumplen condición

Nota: En Python moderno, list comprehensions son más legibles.
Pero map/filter son útiles para funciones como argumentos.
"""

numbers = [5, 12, 18, 21]


# Funciones auxiliares
def multiplier(value: int) -> int:
    """Multiplica valor por sí mismo (cuadrado)."""
    return value * value


def exponential(value: int) -> int:
    """Eleva valor al cubo."""
    return value ** 3


def sum_values(val1: int, val2: int) -> int:
    """Suma dos valores."""
    return val1 + val2


# Opción 1: List comprehension con filtro
# Más legible que map/filter en Python moderno
squared = [multiplier(number) for number in numbers if number > 15]
print(squared)

# Opción 2: map() - aplica función a cada elemento
squared2 = list(map(multiplier, numbers))
print(squared2)

# Opción 3: filter() - selecciona elementos que cumplen condición
# Usa lambda para condición inline
large_values = list(filter(lambda value: value >= 15, numbers))
print(large_values)

# Opción 4: Combinar map + filter
# Primero filtra, después transforma
squared3 = list(map(lambda value: value * value, large_values))
print(squared3)
