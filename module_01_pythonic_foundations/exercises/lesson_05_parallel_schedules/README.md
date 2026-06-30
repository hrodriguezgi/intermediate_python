# Exercise · Parallel Schedules

Implementa una función que combine datos paralelos (lecciones, duraciones, instructores)
en un calendario estructurado.

## Problema

Tienes 3 listas paralelas con información sobre lecciones:
- Nombres de temas
- Duraciones en minutos
- Instructores asignados

Necesitas emparejar estos datos y retornar un calendario donde cada lección tenga:
- Número de lección (1-indexed)
- Tema
- Duración
- Instructor

**Por qué importa:** En pipelines ETL, frecuentemente tienes datos fragmentados
en múltiples fuentes. Necesitas emparejarlos sin usar índices manualmente.

## Objetivos

- **`zip`:** Combina múltiples iterables en paralelo
- **`enumerate`:** Agrega números a una secuencia
- **Data pairing:** Relaciona datos de múltiples fuentes sin índices explícitos
- **Structure assembly:** Construye dictionaries a partir de datos emparejados
- **Real-world pattern:** Típico en procesamiento de archivos/APIs/CSVs

## Entrada de ejemplo

```python
topics = ["Variables", "Funciones", "SQLite"]
durations = [45, 60, 90]
instructors = ["Ana", "Luis", "Marta"]

schedule = build_lesson_schedule(topics, durations, instructors)

# Resultado esperado:
# [
#     {"number": 1, "topic": "Variables", "minutes": 45, "instructor": "Ana"},
#     {"number": 2, "topic": "Funciones", "minutes": 60, "instructor": "Luis"},
#     {"number": 3, "topic": "SQLite", "minutes": 90, "instructor": "Marta"},
# ]
```

## Detalles

- Las lecciones deben estar numeradas empezando en 1
- El diccionario de cada lección debe tener exactamente esos 4 keys
- Usa `zip()` para emparejar datos paralelos
- Usa `enumerate()` para agregar números

## Edge cases

- ¿Qué pasa si las listas tienen longitudes diferentes?
- ¿Qué pasa si alguna lista está vacía?

## Pistas

- `zip(topics, durations, instructors)` empareja los 3 iterables
- `enumerate(..., start=1)` agrega números comenzando en 1
- Combina ambas: `enumerate(zip(...))`
- En el bucle: `for number, (topic, minutes, instructor) in enumerate(zip(...))`
- Esto es elegante porque evita índices manuales como `for i in range(len(...))`
