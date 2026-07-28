# Exercise · Task Registry

## Objetivo

Practicar:
- Constructores (`__init__`) para inicializar objetos
- Métodos dunder (`__repr__`, `__len__`) para integración con Python
- Dataclass como simplificación de `__init__`

## Problema

Crea un sistema de registro de tareas donde:

1. **Clase `Task`:** Representa una tarea individual
   - Atributos: `title`, `completed` (por defecto False)
   - Implementa `__repr__()` para mostrar: `Task(title='...', completed=True/False)`

2. **Clase `TaskRegistry`:** Gestiona colección de tareas
   - Método `add(task)`: Agrega una tarea
   - Método `pending_count()`: Retorna cantidad de tareas incompletas
   - Método `completed_count()`: Retorna cantidad de tareas completadas
   - Implementa `__len__()` para usar `len(registry)` → total de tareas
   - Implementa `__repr__()` para mostrar: `TaskRegistry(N tasks, M pending)`

## Restricciones

- Task puede ser una clase normal O usar `@dataclass` (ambas funcionan)
- TaskRegistry debe ser clase normal (practica `__init__` explícito)
- Implementa todos los dunder methods pedidos

## Ejemplo de Uso

```python
registry = TaskRegistry()
registry.add(Task("Comprar leche"))
registry.add(Task("Estudiar OOP", completed=True))
registry.add(Task("Hacer ejercicio"))

print(len(registry))           # 3
print(registry)                # TaskRegistry(3 tasks, 2 pending)
print(registry.pending_count()) # 2
```
