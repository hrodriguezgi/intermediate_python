# %% [markdown]
# # 01. Patrones de control de flujo
#
# ## Objetivos
#
# - Escribir condicionales con reglas claras.
# - Evitar ramas innecesarias.
# - Usar guard clauses para reducir anidación.
# - Aplicar el operador walrus (`:=`) para validación en bucles.
# - Usar `match` para lógica basada en patrones complejos.

# %%
orders = [
    {"id": 101, "total": 45, "status": "paid"},
    {"id": 102, "total": 5, "status": "pending"},
    {"id": 103, "total": 120, "status": "paid"},
]

# %% [markdown]
# ## Guard clauses
#
# Primero se resuelven los casos que bloquean el flujo normal.


# %%
def classify_order(order: dict) -> str:
    if order["status"] != "paid":
        return "blocked"
    if order["total"] >= 100:
        return "priority"
    if order["total"] >= 20:
        return "standard"
    return "low_value"


for order in orders:
    print(order["id"], classify_order(order))

# %% [markdown]
# ## `for` + acumuladores
#
# Todavía es un patrón útil cuando necesitas varias métricas al mismo tiempo.

# %%
priority_ids = []
blocked_ids = []

for order in orders:
    category = classify_order(order)
    if category == "priority":
        priority_ids.append(order["id"])
    elif category == "blocked":
        blocked_ids.append(order["id"])

print(priority_ids)
print(blocked_ids)

# %% [markdown]
# ## `match` para patrones simples
#
# En Python 3.10 puedes expresar reglas discretas de forma más directa cuando
# los casos dependen de patrones bien definidos.


# %%
def action_for_status(status: str) -> str:
    match status:
        case "paid":
            return "ship"
        case "pending":
            return "wait"
        case "cancelled":
            return "archive"
        case _:
            return "review"


print(action_for_status("paid"))
print(action_for_status("cancelled"))

# %% [markdown]
# ## `match` para patrones complejos
#
# En pipelines de datos reales, necesitas validar y extraer datos de estructuras
# anidadas (eventos de APIs, mensajes de colas, respuestas JSON). `match` maneja
# esto de forma legible.


# %%
# Real scenario: Procesar eventos de una cola de mensajes
events_queue = [
    {"type": "payment", "amount": 150, "currency": "USD"},
    {"type": "refund", "amount": 50},
    {"type": "transfer", "from_account": "123", "to_account": "456", "amount": 200},
    {"type": "unknown_event", "data": {}},
]


def process_event(event: dict) -> str:
    match event:
        case {"type": "payment", "amount": int(amt) | float(amt), "currency": cur}:
            return f"Processing payment: ${amt} {cur}"
        case {"type": "refund", "amount": int(amt) | float(amt)}:
            return f"Processing refund: ${amt}"
        case {"type": "transfer", "from_account": from_acc, "to_account": to_acc}:
            return f"Processing transfer: {from_acc} -> {to_acc}"
        case {"type": t}:
            return f"Unknown event type: {t}"
        case _:
            return "Invalid event structure"


for event in events_queue:
    print(process_event(event))

# %% [markdown]
# ## El operador walrus (`:=`) en validación
#
# El operador walrus permite asignar y validar en una sola expresión. Es especialmente
# útil en bucles de procesamiento donde necesitas validar datos antes de procesarlos.


# %%
# Real scenario: Leer datos línea por línea hasta encontrar EOF o error
import io


def process_log_lines(log_content: str) -> int:
    lines = iter(log_content.split("\n"))
    processed = 0

    # Sin walrus (tedioso)
    # while True:
    #     line = next(lines, None)
    #     if not line:
    #         break
    #     if line.startswith("ERROR"):
    #         print(f"Error line: {line}")
    #         processed += 1

    # Con walrus (elegante y claro)
    while line := next(lines, None):
        if line.startswith("ERROR"):
            print(f"Error line: {line}")
            processed += 1

    return processed


log_data = """INFO: Server started
ERROR: Connection timeout
INFO: Request processed
ERROR: Database locked
INFO: Shutdown
"""

count = process_log_lines(log_data)
print(f"Total errors: {count}")

# %% [markdown]
# ## Walrus en validación de datos
#
# Es especialmente útil cuando validas datos y necesitas usar el resultado validado.


# %%
# Real scenario: Procesar un lote de datos CSV con validación
def validate_and_process(row: dict) -> tuple[bool, str]:
    if (age := row.get("age")) is None:
        return False, "Missing age field"
    if not isinstance(age, int) or age < 0:
        return False, f"Invalid age: {age}"
    if name := row.get("name", "").strip():
        return True, f"Valid: {name} ({age} years old)"
    return False, "Missing or empty name"


csv_rows = [
    {"name": "Ana", "age": 28},
    {"name": "", "age": 35},
    {"name": "Luis", "age": -5},
    {"name": "Marta", "age": None},
]

for row in csv_rows:
    valid, message = validate_and_process(row)
    print(f"  {message}")

# %% [markdown]
# ## Resumen
#
# - Las guard clauses simplifican la lectura.
# - Un buen acumulador evita múltiples recorridos innecesarios.
# - `match` funciona bien para reglas discretas con extracción de datos.
# - El operador walrus (`:=`) es ideal para validación en bucles y expresiones.
