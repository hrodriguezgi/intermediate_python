# Exercise · Inventory Summary

Implementa una función que reciba una lista de productos y construya un resumen
de inventario con totales por categoría.

## Objetivos

- Iterar sobre listas de diccionarios.
- Acumular valores numéricos (stock total).
- Usar un conjunto (`set`) para coleccionar categorías únicas.
- Construir un diccionario de agregación por categoría.
- Combinar múltiples estructuras de datos en una salida coherente.

## Resultado esperado

La función debe retornar un diccionario con:

```python
{
    "total_products": 6,
    "total_stock": 178,
    "categories": ["books", "digital", "hardware"],
    "by_category": {
        "hardware": 25,
        "digital": 150,
        "books": 3
    }
}
```
