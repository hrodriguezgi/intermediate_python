from functools import partial

# TODO: Implementa estas funciones base (flexible y reutilizable)


def convert_to_float(value: str) -> float:
    """Convierte string a float. Maneja excepciones."""
    # Tu código aquí
    pass


def apply_multiplier(value: float, factor: float) -> float:
    """Aplica un multiplicador (impuesto, descuento, conversión)."""
    # Tu código aquí
    pass


def round_price(value: float, decimals: int = 2) -> float:
    """Redondea a decimales específicos."""
    # Tu código aquí
    pass


def apply_transformations(value: str, *transforms) -> float:
    """Aplica múltiples transformaciones en secuencia."""
    # Tu código aquí
    # Pista: comienza convertiendo el valor, luego aplica cada transform
    pass


# TODO: Crea transformaciones parciales reutilizables
# Ejemplo (descomentar y completar):
# apply_tax_19 = partial(...)
# apply_tax_21 = partial(...)
# apply_discount_10 = partial(...)


if __name__ == "__main__":
    # Casos de prueba

    # Caso 1: Precio simple con impuesto 19%
    # Entrada: "100" → Salida: 119.0
    result1 = None  # TODO: Usar apply_transformations con apply_tax_19
    print(f"Test 1 - Precio con 19% impuesto: {result1}")

    # Caso 2: Múltiples transformaciones (impuesto + descuento)
    # Entrada: "100" → Aplicar 19% impuesto → Aplicar 10% descuento
    # Salida: 107.1 (119 * 0.9)
    result2 = None  # TODO: Usar transformaciones múltiples
    print(f"Test 2 - Precio con impuesto y descuento: {result2}")

    # Caso 3: Precios con diferentes impuestos (países diferentes)
    prices = ["50", "75.5", "200"]
    # TODO: Procesa cada precio con apply_tax_21
    # Salida esperada: [60.5, 91.455, 242.0] (redondeado a 2 decimales)
    results3 = None
    print(f"Test 3 - Múltiples precios con 21% impuesto: {results3}")
