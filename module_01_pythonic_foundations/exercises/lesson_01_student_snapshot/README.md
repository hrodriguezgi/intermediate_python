# Exercise · Student Snapshot

Completa `starter.py` para construir un resumen de estudiantes a partir de una
lista de tuplas.

## Problema

Tienes una lista de registros estudiantiles (tuplas de nombre, track, años de experiencia)
y necesitas generar un resumen que responda preguntas comunes de gestión:
- ¿Cuántos estudiantes tenemos?
- ¿Qué tracks están representados?
- ¿Cuál es el promedio de experiencia?

## Objetivos

- **Desempaque de tuplas:** Extrae componentes de tuplas en un bucle
- **Inmutabilidad:** No modifiques la lista original; construye nuevas estructuras
- **Composición de estructuras:** Arma un diccionario que agregue y organice datos
- **Manejo de casos límite:** ¿Qué pasa si la lista está vacía?

## Resultado esperado

La función `build_student_snapshot()` debe retornar un diccionario con:

```python
{
    "total_students": <int>,           # Total de estudiantes
    "tracks": [<str>, ...],            # Lista ORDENADA de tracks únicos
    "experience_average": <float>,     # Promedio redondeado a 2 decimales
}
```

## Entrada de ejemplo

```python
records = [
    ("Ana", "backend", 2),
    ("Luis", "data", 4),
    ("Marta", "backend", 3),
]
# Resultado:
# {
#     "total_students": 3,
#     "tracks": ["backend", "data"],
#     "experience_average": 3.0
# }
```

## Pistas

- Usa desempaque para extraer componentes: `name, track, years = record`
- Un `set` es útil para tracks únicos
- `sum()` o un bucle pueden calcular años totales
- Ordena los tracks antes de retornarlos
- Maneja el caso vacío (lista sin registros)
