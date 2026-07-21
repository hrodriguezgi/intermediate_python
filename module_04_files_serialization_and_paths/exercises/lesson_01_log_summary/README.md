# Exercise · Log Summary

Lee un archivo de logs y retorna un resumen por nivel (`INFO`, `WARNING`,
`ERROR`).

## Notas de Implementación

La solución usa `read_text().splitlines()` que está bien para logs pequeños.
Para logs reales (100GB+), usa la técnica de streaming mostrada en la lección:

```python
with path.open(encoding="utf-8") as f:
    for line in f:  # Procesa línea por línea
        if "ERROR" in line:
            count += 1
```

Esto mantiene memoria constante sin importar el tamaño del archivo.
