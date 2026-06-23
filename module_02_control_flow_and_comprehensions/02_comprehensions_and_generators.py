# %% [markdown]
# # 02. Comprehensions y generadores
#
# ## Objetivos
#
# - Usar comprehensions cuando la transformación es simple.
# - Introducir generadores para no materializar datos innecesarios.

# %%
events = [
    {"user": "ana", "duration": 35, "status": "ok"},
    {"user": "luis", "duration": 12, "status": "retry"},
    {"user": "marta", "duration": 48, "status": "ok"},
    {"user": "ana", "duration": 20, "status": "ok"},
]

# %% [markdown]
# ## List comprehensions

# %%
successful_durations = [
    event["duration"] for event in events if event["status"] == "ok"
]
print(successful_durations)

# %% [markdown]
# ## Dict comprehensions

# %%
latest_duration_by_user = {event["user"]: event["duration"] for event in events}
print(latest_duration_by_user)

# %% [markdown]
# ## Set comprehensions

# %%
active_users = {event["user"] for event in events if event["duration"] >= 20}
print(active_users)

# %% [markdown]
# ## Generadores
#
# Son una buena opción para procesar secuencias largas sin cargar todo en memoria.


# %%
def durations_over(limit: int):
    for event in events:
        if event["duration"] > limit:
            yield event["duration"]


for duration in durations_over(20):
    print(duration)

# %%
total_duration = sum(event["duration"] for event in events if event["status"] == "ok")
print(total_duration)

# %% [markdown]
# ## Resumen
#
# - Las comprehensions funcionan bien para una transformación puntual.
# - Los generadores ayudan a escalar el procesamiento.
