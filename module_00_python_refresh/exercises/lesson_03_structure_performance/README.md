# Exercise · Structure Performance Matters

Implementa dos versiones de una función de deduplicación: una con `list` y otra con `set`.
Compara el rendimiento y entiende por qué la elección de estructura importa en datos grandes.

## Objetivos

- Entender las implicaciones de rendimiento de list vs set.
- Practicar usar `set` para deduplicación eficiente.
- Medir rendimiento con `timeit` (introducción a profiling).
- Reconocer cuándo aplicar la estructura correcta en datos reales.

## Contexto Real

En pipelines de ETL que procesan millones de registros, elegir la estructura correcta
puede ser la diferencia entre segundos y minutos. Este ejercicio muestra por qué.

## Tarea

Implementa dos funciones en `starter.py`:

### 1. `deduplicate_with_list(ids: list[int]) -> list[int]`
- Retorna una lista de IDs únicos usando solo `list`.
- Usa un loop para verificar si cada ID está en la lista antes de agregarlo.
- Implementación ingenua pero correcta.

### 2. `deduplicate_with_set(ids: list[int]) -> list[int]`
- Retorna una lista de IDs únicos usando `set`.
- Más eficiente: convierte a set, luego retorna como lista.

### 3. Comparación (en el `if __name__ == "__main__"` block)
- Crea una lista de 100,000 IDs con duplicados.
- Mide el tiempo que tarda cada función con `timeit`.
- Imprime los resultados mostrando el speedup.

## Resultado Esperado

```
Deduplicating 100,000 IDs:
List approach: 4.2534s
Set approach: 0.0123s
Set es ~346x más rápido
```

## Pistas

- Importa `timeit` del módulo `timeit`
- Usa `timeit.timeit(lambda: func(), number=10)` para medir
- La diferencia será dramática para 100K+ items
