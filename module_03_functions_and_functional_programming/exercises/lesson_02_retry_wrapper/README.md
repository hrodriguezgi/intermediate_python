# Exercise · Retry Wrapper con Logging

## Objetivo
Implementa un decorador que reintente una función fallida y registre los intentos.
Combina el patrón de decorador con logging y monitoreo.

## Requisitos

Implementa un decorador `@retry` que:
1. Reintente la función hasta `n` veces si genera una excepción
2. Registre cada intento (logging)
3. Mida el tiempo total de ejecución
4. Proporcione información útil en caso de fallo

## Escenario Real
En pipelines de datos, las conexiones fallan ocasionalmente:
- API responde con timeout (reintenta automáticamente)
- Conexión a BD cae (reintenta después de esperar)
- Descarga de archivo falla (reintenta con backoff)

El decorador debe permitir que estas funciones se recuperen automáticamente.

## Estructura esperada
```python
@retry(times=3)
def fetch_data_from_api(url: str) -> dict:
    # Simula fallos ocasionales
    # En el intento 3, debe funcionar
    pass

# Uso:
result = fetch_data_from_api("https://api.example.com/data")
# Si falla en intento 1 y 2, reintenta en intento 3
# Registra logs: "Intento 1/3", "Intento 2/3", etc.
```

## Comportamiento esperado
```
Intento 1/3: fetch_data_from_api(https://api.example.com/data) - Falló (ValueError: API no disponible)
Intento 2/3: fetch_data_from_api(https://api.example.com/data) - Falló (ValueError: API no disponible)
Intento 3/3: fetch_data_from_api(https://api.example.com/data) - Éxito (2.45s)
 Completado en 2.45s
```

## Notas
- Usa `functools.wraps` para preservar metadatos
- Imprime logs de cada intento
- Registra el tiempo total con `time.perf_counter()`
- Si todos los intentos fallan, relanza la última excepción
