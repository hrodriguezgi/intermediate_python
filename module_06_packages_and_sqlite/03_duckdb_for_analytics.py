# %% [markdown]
# # 03. DuckDB para Analytics
#
# ## Objetivos
#
# - Entender DuckDB vs SQLite: trade-offs
# - Cargar y procesar datos con DuckDB
# - Escribir queries analíticas (GROUP BY, JOIN, agregaciones)
# - Entender cuándo usar cada base de datos

# %% [markdown]
# ## SQLite vs DuckDB
#
# | Aspecto | SQLite | DuckDB |
# |--------|--------|--------|
# | Propósito | Aplicaciones transaccionales | Análisis de datos |
# | Optimizado para | Escrituras pequeñas, ACID | Lecturas masivas, cálculos |
# | Almacenamiento | Archivo en disco | Memoria (o disco) |
# | Velocidad queries | Buena para pequeños datos | **EXCELENTE para millones** |
# | Compresión | No | **Sí (vectorized)** |
# | Concurrencia | 1 escritor | Múltiples lectores |
#
# **Regla:** SQLite = transaccional, DuckDB = analítico

# %% [markdown]
# ## Instalación y conexión
#
# DuckDB es simple: un archivo `.duckdb` o en memoria con `:memory:`

# %%
import duckdb
from pathlib import Path
import csv
import tempfile

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "analytics.duckdb"

# Conexión a archivo (persistente)
conn = duckdb.connect(str(DB_PATH))

print(f"DuckDB connected to: {DB_PATH}")

# %% [markdown]
# ## Cargar CSV en DuckDB
#
# DuckDB es experto en leer CSV. Sin intermediarios.

# %%
# Crear CSV de prueba
sample_csv = BASE_DIR / "data" / "sales.csv"
sample_csv.parent.mkdir(exist_ok=True)

csv_data = """date,product,quantity,price,region
2024-01-01,Laptop,2,1500,North
2024-01-02,Mouse,50,25,South
2024-01-03,Keyboard,30,75,East
2024-01-04,Laptop,1,1500,West
2024-01-05,Monitor,15,400,North
2024-01-06,Mouse,100,25,South
2024-01-07,Keyboard,40,75,East"""

sample_csv.write_text(csv_data)

# Leer CSV directamente (sin pandas!)
result = conn.execute(f"SELECT * FROM read_csv_auto('{sample_csv}')").fetchall()
print(f"CSV loaded: {len(result)} rows")

# %% [markdown]
# ## Viendo esquema de datos
#
# DuckDB autodetecta tipos de datos del CSV.

# %%
# Get schema by creating a temporary view
conn.execute(f"CREATE TEMP VIEW csv_preview AS SELECT * FROM read_csv_auto('{sample_csv}')")
schema = conn.execute("DESCRIBE csv_preview").fetchall()
print("\nCSV Schema:")
for col_name, col_type, *_ in schema:
    print(f"  {col_name}: {col_type}")

# %% [markdown]
# ## Queries analíticas
#
# Agregar, agrupar, filtrar: igual que SQL pero **mucho más rápido** en millones de filas.

# %%
# Total de ventas por producto
sales_by_product = conn.execute(f"""
    SELECT
        product,
        COUNT(*) as transactions,
        SUM(quantity) as total_qty,
        SUM(quantity * price) as revenue
    FROM read_csv_auto('{sample_csv}')
    GROUP BY product
    ORDER BY revenue DESC
""").fetchall()

print("\nSales by Product:")
for product, trans, qty, revenue in sales_by_product:
    print(f"  {product}: {trans} trans, {qty} units, ${revenue:.2f}")

# %% [markdown]
# ## Queries por región
#
# Análisis geográfico rápido.

# %%
regional_analysis = conn.execute(f"""
    SELECT
        region,
        COUNT(*) as transactions,
        AVG(quantity * price) as avg_transaction,
        SUM(quantity * price) as total_revenue
    FROM read_csv_auto('{sample_csv}')
    GROUP BY region
    ORDER BY total_revenue DESC
""").fetchall()

print("\nSales by Region:")
for region, trans, avg_trans, revenue in regional_analysis:
    print(f"  {region}: {trans} trans, avg ${avg_trans:.2f}, total ${revenue:.2f}")

# %% [markdown]
# ## Crear tabla persistente desde CSV
#
# Guardar datos en el duckdb file para queries rápidas después.

# %%
conn.execute(f"""
    CREATE TABLE sales AS
    SELECT * FROM read_csv_auto('{sample_csv}')
""")

print("Table 'sales' created in DuckDB")

# Verificar
tables = conn.execute("SHOW TABLES").fetchall()
print(f"Tables in database: {[t[0] for t in tables]}")

# %% [markdown]
# ## Queries en tabla persistente (mucho más rápido)
#
# Cuando los datos están en DuckDB, queries son casi instantáneas.

# %%
# Top 3 transacciones más altas
top_transactions = conn.execute("""
    SELECT
        date,
        product,
        quantity,
        price,
        (quantity * price) as total
    FROM sales
    ORDER BY total DESC
    LIMIT 3
""").fetchall()

print("\nTop 3 Transactions:")
for date, product, qty, price, total in top_transactions:
    print(f"  {date}: {qty}x {product} @ ${price} = ${total:.2f}")

# %% [markdown]
# ## Análisis temporal
#
# Tendencias por fecha.

# %%
daily_revenue = conn.execute("""
    SELECT
        date,
        COUNT(*) as transactions,
        SUM(quantity * price) as daily_revenue
    FROM sales
    GROUP BY date
    ORDER BY date
""").fetchall()

print("\nDaily Revenue:")
for date, trans, revenue in daily_revenue:
    print(f"  {date}: {trans} trans, ${revenue:.2f}")

# %% [markdown]
# ## Comparativas: SQLite vs DuckDB en velocidad
#
# Simulemos con un dataset más grande.

# %%
import time

# Crear dataset grande (10k filas)
large_csv = BASE_DIR / "data" / "large_sales.csv"

print("\nCreating large dataset (10k rows)...")
with open(large_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "product", "quantity", "price", "region"])

    products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"]
    regions = ["North", "South", "East", "West"]

    for i in range(10000):
        product = products[i % len(products)]
        region = regions[i % len(regions)]
        qty = (i % 100) + 1
        price = 25 + (i % 1500)
        writer.writerow([f"2024-01-{(i % 28) + 1:02d}", product, qty, price, region])

print(f"Large CSV created: {large_csv.stat().st_size / 1024:.1f} KB")

# %% [markdown]
# ## Query en dataset grande
#
# DuckDB maneja esto sin problemas (SQLite también, pero DuckDB es más rápido).

# %%
# Top productos por región (con dataset grande)
start = time.perf_counter()

top_by_region = conn.execute(f"""
    SELECT
        region,
        product,
        SUM(quantity * price) as revenue,
        COUNT(*) as transactions
    FROM read_csv_auto('{large_csv}')
    GROUP BY region, product
    ORDER BY region, revenue DESC
""").fetchall()

elapsed = time.perf_counter() - start

print(f"\nQuery on 10k rows completed in {elapsed*1000:.2f}ms")
print(f"Results: {len(top_by_region)} product-region combinations")

# %% [markdown]
# ## Ventaja de vectorización: DuckDB vs pandas
#
# DuckDB no carga TODO en memoria (usa vectorized processing).

# %%
print("\n=== Comparación de enfoque ===")

print("\nPandas approach:")
print("  CSV -> DataFrame (carga TODO en RAM) -> analizar")
print("  Rápido para pequeños datos, lento para grandes")

print("\nDuckDB approach:")
print("  CSV -> Query (procesa por bloques) -> resultado")
print("  Eficiente en memoria, velocidad consistente")

# %% [markdown]
# ## Exportar resultados
#
# DuckDB puede guardar resultados como CSV, JSON, o tabla.

# %%
# Guardar análisis como CSV
output_csv = BASE_DIR / "data" / "analysis_results.csv"

conn.execute(f"""
    COPY (
        SELECT
            region,
            product,
            SUM(quantity * price) as revenue
        FROM read_csv_auto('{large_csv}')
        GROUP BY region, product
        ORDER BY revenue DESC
    ) TO '{output_csv}' (FORMAT CSV, HEADER)
""")

print(f"\nResults exported to: {output_csv}")

# %% [markdown]
# ## Cuándo usar cada base de datos
#
# **Usa SQLite cuando:**
# - Necesitas ACID (transacciones, consistency)
# - Una aplicación escribe/lee datos simultáneamente
# - Los datos son pequeños (< 1GB)
# - Necesitas un archivo simple para compartir
#
# **Usa DuckDB cuando:**
# - Analizas datos históricos (sin actualizaciones frecuentes)
# - Trabajas con millones de filas
# - Necesitas queries rápidas en datos densos
# - Procegas CSV/JSON grandes
# - Haces ciencia de datos o BI
#
# **Usa PostgreSQL cuando:**
# - Múltiples aplicaciones escriben datos
# - Datos críticos (financieros, médicos)
# - Necesitas replicación o backup
# - Escala a petabytes

# %% [markdown]
# ## Resumen
#
# - **DuckDB:** Base de datos analítica, no transaccional
# - **Velocidad:** 10-100x más rápido que SQLite en queries analíticas
# - **Memoria:** Vectorized processing, eficiente
# - **CSV:** Carga CSV directamente sin intermediarios
# - **Trade-off:** No es bueno para actualizaciones frecuentes (SQLite sí)
#
# Próximo: FastAPI para exponer todos estos datos como API.

# %%
conn.close()
print("\nDuckDB connection closed")
