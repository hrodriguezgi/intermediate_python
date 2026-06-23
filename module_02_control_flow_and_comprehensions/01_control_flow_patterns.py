# %% [markdown]
# # 01. Patrones de control de flujo
#
# ## Objetivos
#
# - Escribir condicionales con reglas claras.
# - Evitar ramas innecesarias.
# - Usar guard clauses para reducir anidación.

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
# ## `match`
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
# ## Resumen
#
# - Las guard clauses simplifican la lectura.
# - Un buen acumulador evita múltiples recorridos innecesarios.
# - `match` funciona bien para reglas discretas.
