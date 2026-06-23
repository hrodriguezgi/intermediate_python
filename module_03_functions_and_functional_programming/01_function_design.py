# %% [markdown]
# # 01. Diseño de funciones
#
# ## Objetivos
#
# - Separar responsabilidades.
# - Definir funciones con entradas y salidas claras.
# - Reducir efectos secundarios.

# %%
from statistics import mean

scores = [88, 91, 74, 100, 95]

# %% [markdown]
# ## Funciones puras
#
# Una función pura depende sólo de sus argumentos y retorna un valor nuevo.


# %%
def normalize_score(score: int, max_score: int = 100) -> float:
    return round(score / max_score, 2)


normalized_scores = [normalize_score(score) for score in scores]
print(normalized_scores)

# %% [markdown]
# ## Funciones con nombre claro


# %%
def build_grade_report(raw_scores: list[int]) -> dict:
    return {
        "count": len(raw_scores),
        "average": round(mean(raw_scores), 2),
        "max": max(raw_scores),
        "min": min(raw_scores),
    }


print(build_grade_report(scores))

# %% [markdown]
# ## `*args` y `**kwargs`
#
# Úsalos cuando aportan flexibilidad real, no por costumbre.


# %%
def format_labels(*labels: str, uppercase: bool = False) -> list[str]:
    if uppercase:
        return [label.upper() for label in labels]
    return [label.title() for label in labels]


print(format_labels("python", "sqlite", uppercase=True))

# %% [markdown]
# ## Resumen
#
# - Una función pequeña es más fácil de validar.
# - Un nombre claro comunica la intención.
# - `*args` y `**kwargs` deben usarse con criterio.
