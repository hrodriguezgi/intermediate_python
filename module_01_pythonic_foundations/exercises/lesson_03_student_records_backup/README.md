# Exercise · Student Records Backup

Implementa una función que cree una copia segura de registros de estudiantes, evitando
el trap de referencias compartidas.

## Problema

Eres responsable de hacer backup de registros estudiantiles antes de cualquier migración.
Tienes una lista de dictionaries con información de estudiantes y necesitas:

1. Crear una copia que se pueda modificar sin afectar el original
2. Manejar datos anidados (los estudiantes tienen un diccionario de metadata)
3. Verificar que realmente sea una copia independiente

**El trap:** Una copia superficial (`list()` o `[:]`) NO es suficiente cuando los elementos
son diccionarios u otros objetos mutables. Las estructuras anidadas seguirán compartiendo
referencias.

## Objetivos

- **Mutabilidad vs Inmutabilidad:** Entender qué objetos son mutables/inmutables
- **Referencias compartidas:** Evitar aliasing accidental en datos complejos
- **Shallow vs Deep copy:** Saber cuándo cada una es suficiente o peligrosa
- **Copias seguras:** Implementar backup de datos anidados sin mutaciones
- **Testing de independencia:** Verificar que el original no se afecta

## Contexto: Por qué importa

En pipelines de datos reales:
- Recibes un dataset y necesitas transformar una copia sin perder el original
- Los registros tienen metadatos anidados (diccionarios, objetos)
- Una copia superficial parece funcionar... hasta que modifica datos anidados y rompe el
  original en producción

## Entrada de ejemplo

```python
students = [
    {
        "id": 1,
        "name": "Ana",
        "metadata": {"track": "backend", "years": 2}
    },
    {
        "id": 2,
        "name": "Luis",
        "metadata": {"track": "data", "years": 4}
    },
]

backup = create_student_backup(students)

# Modifica el backup
backup[0]["name"] = "Anna"
backup[0]["metadata"]["years"] = 5

# El original DEBE quedar intacto
assert students[0]["name"] == "Ana"
assert students[0]["metadata"]["years"] == 2
```

## Resultado esperado

La función `create_student_backup()` retorna una copia profunda donde:
- Modificar la lista backup NO afecta `students`
- Modificar diccionarios dentro del backup NO afecta `students`
- Modificar valores anidados NO afecta `students`

## Pistas

- `import copy` proporciona `copy.deepcopy()`
- `deepcopy()` crea una copia recursiva de TODA la estructura
- Una copia superficial con `list()` NO es suficiente aquí
- Prueba modificar el backup y verifica que el original no cambia
- ¿Qué pasa si usas `list()` o `[:]`? ¡Es el trap!
