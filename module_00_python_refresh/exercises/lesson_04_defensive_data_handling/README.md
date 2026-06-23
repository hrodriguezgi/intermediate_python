# Exercise · Defensive Data Handling

Los datos reales raramente son "puros". APIs devuelven strings en lugar de números,
CSVs tienen valores faltantes, y la diferencia entre `None` y `[]` importa.
Este ejercicio te prepara para datos desordenados.

## Objetivos

- Entender cuándo distinguir entre `None` y contenedores vacíos.
- Escribir funciones defensivas que manejan tipos inconsistentes.
- Validar datos antes de procesarlos.
- Prepararse para integrar APIs y archivos CSV en la vida real.

## Contexto Real

En ETL:
- APIs devuelven `"123"` en lugar de `123`
- CSVs tienen valores faltantes representados como strings vacíos o `None`
- Un boolean puede venir como `"yes"`, `"true"`, `1`, o `True`
- `None` significa "no enviado", mientras que `[]` significa "enviado pero vacío"

## Tarea

Implementa funciones de conversión defensivas en `starter.py`:

### 1. `safe_parse_int(value, default: int = 0) -> int`
- Convierte `value` a entero de forma segura.
- Si es `None`, retorna `default`.
- Si es string, intenta convertir.
- Si la conversión falla, retorna `default`.

### 2. `safe_parse_bool(value, default: bool = False) -> bool`
- Convierte `value` a booleano de forma segura.
- `None` → `default`
- Strings: `"yes"`, `"true"`, `"1"`, `"on"` → `True` (case-insensitive)
- Otros strings → `False`
- Numbers: 0 → `False`, cualquier otro → `True`

### 3. `parse_user_record(user_data: dict) -> dict`
- Procesa un diccionario de usuario con tipos inconsistentes.
- Valida y convierte:
  - `id`: debe ser int, requerido (no puede ser `None`)
  - `name`: string, requerido, strip y title case
  - `age`: int, opcional (puede ser `None` o `[]`)
  - `active`: bool, default False
  - `tags`: lista de strings (puede ser `None`, string con comas, o lista)
- Retorna un diccionario con tipos correctos.
- Lanza `ValueError` si `id` o `name` son `None` o vacíos.

## Datos de Prueba

```python
users = [
    {"id": 1, "name": "  alice  ", "age": "30", "active": "yes", "tags": "python,data"},
    {"id": "2", "name": "bob", "age": None, "active": True, "tags": []},
    {"id": 3, "name": " charlie ", "age": "invalid", "active": "no", "tags": None},
]
```

## Resultado Esperado

```python
{
    "id": 1,
    "name": "Alice",
    "age": 30,
    "active": True,
    "tags": ["python", "data"]
}
```

## Pistas

- Usa `isinstance(value, type)` para verificar tipos.
- Usa `.strip().lower()` para normalizar strings.
- `try/except` para conversiones que pueden fallar.
- Usa `is None` para distinguir entre `None` y otros "falsy" values.
