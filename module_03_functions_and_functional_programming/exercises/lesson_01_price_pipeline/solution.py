from functools import partial


def convert_to_float(value: str) -> float:
    """Convierte string a float. Maneja excepciones."""
    try:
        return float(value.strip())
    except ValueError as e:
        raise ValueError(f"No se puede convertir '{value}' a float") from e


def apply_multiplier(value: float, factor: float) -> float:
    """Aplica un multiplicador (impuesto, descuento, conversión)."""
    return value * factor


def round_price(value: float, decimals: int = 2) -> float:
    """Redondea a decimales específicos."""
    return round(value, decimals)


def apply_transformations(value: str, *transforms) -> float:
    """Aplica múltiples transformaciones en secuencia."""
    result = convert_to_float(value)
    for transform in transforms:
        result = transform(result)
    return result


# Crea transformaciones parciales reutilizables
apply_tax_19 = partial(apply_multiplier, factor=1.19)
apply_tax_21 = partial(apply_multiplier, factor=1.21)
apply_tax_7 = partial(apply_multiplier, factor=1.07)
apply_discount_10 = partial(apply_multiplier, factor=0.90)
apply_discount_15 = partial(apply_multiplier, factor=0.85)
round_to_2 = partial(round_price, decimals=2)


if __name__ == "__main__":
    # Caso 1: Precio simple con impuesto 19%
    result1 = apply_transformations("100", apply_tax_19, round_to_2)
    print(f"Test 1 - Precio con 19% impuesto: {result1}")
    assert result1 == 119.0

    # Caso 2: Múltiples transformaciones (impuesto + descuento)
    result2 = apply_transformations("100", apply_tax_19, apply_discount_10, round_to_2)
    print(f"Test 2 - Precio con impuesto y descuento: {result2}")
    assert result2 == 107.1

    # Caso 3: Precios con diferentes impuestos (países diferentes)
    prices = ["50", "75.5", "200"]
    results3 = [
        apply_transformations(price, apply_tax_21, round_to_2)
        for price in prices
    ]
    print(f"Test 3 - Múltiples precios con 21% impuesto: {results3}")
    assert results3 == [60.5, 91.36, 242.0]

    print("\n✓ Todos los tests pasaron!")
