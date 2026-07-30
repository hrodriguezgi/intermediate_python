def create_data_processor(transformation_rules: dict):
    """
    Crea un procesador de datos personalizado.

    Cada procesador aplica transformaciones específicas a campos.
    Reutilizable para múltiples registros/lotes.
    """

    def process(record: dict) -> dict:
        """Aplica transformaciones a un registro."""
        result = record.copy()
        for field, transform in transformation_rules.items():
            if field in result and result[field] is not None:
                try:
                    result[field] = transform(result[field])
                except Exception as e:
                    raise ValueError(f"Error transformando {field}: {e}")
        return result

    return process


# Caso 1: Procesar datos de usuarios
# Nota: lambda permite combinar múltiples transformaciones
user_processor = create_data_processor(
    {
        "email": lambda x: str.strip(x).lower(),  # Limpiar y minúsculas
        "name": str.strip,  # Quitar espacios en blanco
        "age": int,  # Convertir a entero
    }
)

print(type(user_processor), user_processor({"email": "  MASD@mail.com ", "name": "  Harvey ", "age": "10"}))
