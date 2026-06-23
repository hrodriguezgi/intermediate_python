# %% [markdown]
# # 02. Excepciones y validación
#
# ## Objetivos
#
# - Fallar con mensajes útiles.
# - Crear excepciones específicas cuando aporta claridad.

# %%
class EnrollmentError(Exception):
    pass


def enroll_student(student_name: str, seats_left: int) -> str:
    if not student_name.strip():
        raise EnrollmentError("student_name cannot be empty")
    if seats_left <= 0:
        raise EnrollmentError("no seats available")
    return f"{student_name} enrolled"


try:
    print(enroll_student("Ana", 2))
    print(enroll_student("", 1))
except EnrollmentError as error:
    print("Enrollment failed:", error)

# %% [markdown]
# ## Resumen
#
# - No todas las validaciones deben retornar `False`.
# - Una excepción específica hace más claro el error operacional.
