# Exercise · Price Pipeline with Partial Functions

## Objetivo
Crea una tubería reutilizable de transformación de precios usando `functools.partial` 
y evitando el error de argumentos mutables por defecto.

## Requisitos

Implementa funciones que:
1. Convierta strings a números (con manejo de errores)
2. Aplique múltiples transformaciones en secuencia (impuestos, descuentos, redondeo)
3. Use `functools.partial` para configurar transformaciones reutilizables
4. **NO** use valores mutables por defecto

## Escenario Real
Un sistema de facturación necesita procesar precios de diferentes fuentes:
- Precios en moneda extranjera (aplica tasa de cambio)
- Precios con diferentes impuestos por país (19%, 21%, 7%)
- Precios con descuentos variables (aplica % de descuento)

## Estructura esperada
```python
# Funciones base (flexible, reutilizable)
convert_to_float(value: str) -> float
apply_multiplier(value: float, factor: float) -> float
round_price(value: float, decimals: int) -> float

# Funciones configuradas con partial
# (estudiante debe crear estas usando partial)
apply_tax_19()  # partial para 19% de impuesto
apply_tax_21()  # partial para 21% de impuesto
apply_discount_10()  # partial para 10% de descuento

# Tubería final
apply_transformations(price_str, *transforms)
```

## Ejemplo de uso
```python
# Configurar transformaciones una vez
price_with_tax_19 = partial(apply_multiplier, factor=1.19)
price_with_discount = partial(apply_multiplier, factor=0.90)

# Reutilizar en múltiples lugares
result1 = price_with_tax_19(convert_to_float("100"))
result2 = price_with_discount(result1)
```

## Notas
- No uses listas/diccionarios como argumentos por defecto (❌ `cache=[]`)
- Usa `None` como valor por defecto si necesitas inicializar (✅ `cache=None`)
- Prueba con valores del mundo real: "10.50", "20,99" (con diferentes separadores)
