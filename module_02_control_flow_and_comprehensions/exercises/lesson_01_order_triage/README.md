# Exercise · Order Triage

Clasifica órdenes en `priority`, `standard`, `low_value` y `blocked`.

## Objetivos

- Practicar reglas con guard clauses.
- Consolidar acumuladores.
- Aplicar validación defensiva con datos reales (messy data).
- Usar match statements para lógica discreta (desafío).

## Parte 1: Clasificación básica

Implementa `triage_orders(orders)` que retorna un diccionario con listas de IDs clasificadas:
- `blocked`: órdenes con status != "paid"
- `priority`: status="paid" AND total >= 100
- `standard`: status="paid" AND total >= 20
- `low_value`: status="paid" AND total < 20

## Parte 2: Validación defensiva (desafío)

Los datos reales son messy. Algunas órdenes tienen:
- Valores faltantes (`None`)
- Tipos incorrectos (`"150"` como string en lugar de int)
- Campos inexistentes

Implementa `triage_orders_safe(orders)` que:
1. Valida que cada orden tenga `id`, `total`, y `status`
2. Convierte `total` a número si es string
3. Retorna el mismo diccionario + una clave `invalid` con órdenes rechazadas

Ejemplo:
```python
messy = [
    {"id": 1, "total": 150, "status": "paid"},  # Válida
    {"id": 2, "total": "35", "status": "paid"},  # Total es string
    {"id": 3},  # Falta total y status
    {"id": 4, "total": 20, "status": None},  # Status inválido
]
# Debe clasificar correctamente el 1 y 2, y rechazar 3 y 4
```

## Parte 3: Match statements (desafío avanzado)

En lugar de usar if/elif, implementa `classify_order_match(order)` usando `match` statements
que retorne la categoría: "blocked", "priority", "standard", o "low_value".

Tip: Puedes usar pattern matching para verificar el status y el total en una sola expresión.
