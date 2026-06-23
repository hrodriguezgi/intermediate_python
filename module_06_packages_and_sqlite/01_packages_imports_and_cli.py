# %% [markdown]
# # 01. Paquetes, imports y CLI
#
# ## Objetivos
#
# - Entender cómo organizar código en módulos reutilizables.
# - Introducir una interfaz mínima por línea de comandos.

# %%
from module_06_packages_and_sqlite.shared.text_tools import slugify

title = "Curso de Python Intermedio"
print(slugify(title))

# %% [markdown]
# ## Punto de entrada simple


# %%
def main(name: str) -> None:
    print(f"Hola, {name}. Bienvenido al módulo final.")


if __name__ == "__main__":
    main("equipo")
