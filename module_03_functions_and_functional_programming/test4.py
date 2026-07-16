"""
Lección: functools.partial

Concepto:
partial() crea una nueva función con argumentos pre-configurados.
Útil para crear versiones especializadas de funciones generales.

Ventaja: Define configuración una vez, reutiliza muchas veces.
"""

from functools import partial


def normalize_score(score: int | float, max_score: int) -> float:
    """
    Normaliza un score respecto a un máximo.

    score: Valor a normalizar
    max_score: Valor máximo de la escala
    """
    return round(score / max_score, 2)


# Crea versiones especializadas con partial
# Fija el argumento max_score, score sigue siendo variable
normalizar_5 = partial(normalize_score, max_score=5)
normalizar_10 = partial(normalize_score, max_score=10)

# Caso 1: Normalización de 0 a 5
valores = [3, 5, 4, 4, 5]

# Aplica normalizador de 5
resultado = [normalizar_5(valor) for valor in valores]
print(resultado)


# Caso 2: Normalización de 0 a 10
valores = [3, 5, 4, 4, 5]

# Aplica normalizador de 10 (mismos datos, diferente escala)
resultado = [normalizar_10(valor) for valor in valores]
print(resultado)
