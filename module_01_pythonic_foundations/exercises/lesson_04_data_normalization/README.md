# Exercise · Data Normalization

Implementa una función que normalice y procese datos desordenados de categorías.

## Problema

Recibes datos de un formulario o CSV con categorías/tags en formato inconsistente:
- Espacios extra ("python ", " data")
- Mayúsculas mixtas ("Python", "PYTHON", "python")
- Duplicados ("python,python,data")
- Separadores inconsistentes

Necesitas:
1. Normalizar (minúsculas, sin espacios)
2. Deduplicar (mantener solo únicos)
3. Contar frecuencias
4. Retornar en formato limpio

**Por qué importa:** En pipelines ETL reales, 80% del tiempo se gasta limpiando datos,
no analizándolos. Aprender a procesar texto desordenado es crítico.

## Objetivos

- **String methods:** `strip()`, `split()`, `join()`, `lower()`
- **Normalization:** Convertir datos inconsistentes a formato estándar
- **Deduplication:** Usar `set` para únicos
- **Aggregation:** Usar `Counter` para frecuencias
- **Real-world practice:** Datos como vienen de APIs/CSVs/usuarios

## Entrada de ejemplo

```python
messy_tags = "python, Data , PYTHON,  files,python,data"

result = normalize_and_count_tags(messy_tags)

# Resultado esperado:
# {
#     "unique_tags": ["data", "files", "python"],  # Ordenado
#     "total_unique": 3,
#     "frequencies": {"python": 3, "data": 2, "files": 1},
# }
```

## Detalles del resultado

- **`unique_tags`:** Lista de tags únicos, ordenados alfabéticamente
- **`total_unique`:** Cantidad total de tags únicos
- **`frequencies`:** Diccionario con contador de apariciones de cada tag

## Pistas

- `string.split(",")` divide por separador
- `tag.strip()` elimina espacios
- `tag.lower()` convierte a minúsculas
- `set()` elimina duplicados automáticamente
- `Counter` del módulo `collections` cuenta frecuencias
- Una lista por comprehensión es elegante para procesar
- `sorted()` ordena la lista de tags únicos
