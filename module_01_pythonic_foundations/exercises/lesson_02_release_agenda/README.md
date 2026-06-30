# Exercise · Release Agenda

Implementa una función que planifique el calendario de lanzamiento de módulos.

## Problema

Eres responsable de coordinar la publicación de lecciones en una plataforma de cursos.
Dado una fecha de inicio y un número de lecciones, necesitas:

1. Calcular cuándo se publica cada lección (una por semana)
2. Retornar el calendario completo en un formato estructurado
3. Facilitar que otros sistemas (correos, notificaciones) usen esas fechas

## Objetivos

- **Conversión de texto a fecha:** Convierte strings ISO ("2026-07-01") a objetos `date`
- **Aritmética de fechas:** Calcula offsets (semanas) usando `timedelta`
- **Generación de secuencias:** Crea una lista de fechas futures con un patrón consistente
- **Estructura de datos clara:** Retorna un diccionario con metadata útil

## Resultado esperado

La función `build_release_agenda()` debe retornar un diccionario como:

```python
{
    "start_date": "2026-07-01",         # Fecha de inicio (string ISO)
    "lesson_count": 4,                  # Número de lecciones
    "schedule": [
        "2026-07-01",                   # Lección 1 (semana 0)
        "2026-07-08",                   # Lección 2 (semana 1)
        "2026-07-15",                   # Lección 3 (semana 2)
        "2026-07-22",                   # Lección 4 (semana 3)
    ]
}
```

## Entrada de ejemplo

```python
build_release_agenda("2026-07-01", 4)
```

## Pistas

- `date.fromisoformat("2026-07-01")` convierte texto a objeto `date`
- `date.isoformat()` convierte un `date` de vuelta a string
- `timedelta(days=7 * index)` calcula desplazamientos de semanas
- Una lista por comprehensión es elegante aquí
- El `schedule` debe tener exactamente `lesson_count` fechas
