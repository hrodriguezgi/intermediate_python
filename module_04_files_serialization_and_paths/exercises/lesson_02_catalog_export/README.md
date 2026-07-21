# Exercise · Catalog Export

Lee un CSV de productos y genera un JSON con el total de ítems y la suma del
inventario.

## Desafío Avanzado

Para archivos CSV muy grandes (millones de filas), la carga completa en memoria
puede ser prohibitiva. Revisa la lección sobre "streaming" en
`02_csv_json_and_pickle.py` para aprender cómo procesar fila-por-fila sin cargar
todo en memoria.

En este ejercicio, `list(csv.DictReader(...))` está bien porque el JSON final
necesita todos los ítems. Pero en pipelines reales, muchas veces transformas y
descartas sin guardar todo.
