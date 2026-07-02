# Exercise · Event Digest

Construye un resumen a partir de una lista de eventos.

## Objetivos

- Usar comprehensions para transformar datos.
- Resumir información en un solo paso.
- Entender cuándo usar generators vs list comprehensions (memory efficiency).
- Procesar datos sin cargar todo en memoria (desafío).

## Parte 1: Resumen básico con comprehensions

Implementa `build_event_digest(events)` que retorna un diccionario con:
- `ok_count`: número de eventos con status="ok"
- `users`: lista ordenada de usuarios únicos con eventos "ok"
- `total_duration`: suma de duración de eventos "ok"

## Parte 2: Función eficiente para datos grandes (desafío)

En pipelines reales, procesas millones de eventos. No puedes cargar todo en memoria.

Implementa `build_event_digest_generator(events_iter)` que:
1. Usa expresiones generador (no list comprehensions)
2. Procesa eventos bajo demanda sin cargar todo en memoria
3. Retorna el mismo resumen que Part 1

Tip: Usa generadores para filtrar y transformar, pero necesitarás materializar
los datos finales (lista de usuarios, suma total).

## Parte 3: Procesamiento desde archivo (desafío avanzado)

Implementa `build_event_digest_from_lines(lines)` que:
1. Lee eventos línea por línea (JSON)
2. Usa walrus operator (`:=`) para validar mientras procesa
3. Maneja errores de formato gracefully
4. Retorna el mismo resumen + campo `errors` con líneas inválidas

Ejemplo:
```python
log_lines = [
    '{"user": "ana", "duration": 30, "status": "ok"}',
    '{"user": "luis", "duration": 12, "status": "retry"}',
    'INVALID_JSON',  # Error
    '{"user": "marta", "duration": 48, "status": "ok"}',
]
result = build_event_digest_from_lines(log_lines)
# result['invalid'] debería tener el índice de la línea inválida
```
