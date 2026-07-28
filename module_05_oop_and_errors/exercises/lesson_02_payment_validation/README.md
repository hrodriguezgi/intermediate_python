# Exercise · Payment Validation

## Objetivo

Practicar:
- Custom exceptions con contexto (metadata útil)
- Elegir el tipo correcto de excepción (ValueError, custom)
- Validación con mensajes claros para debugging

## Problema

Crea un sistema de validación de pagos:

1. **Excepción personalizada `PaymentError`**
   - Heredar de `ValueError` (error de validación de entrada)
   - Almacenar: `amount`, `reason` (por qué falló)
   - Mensaje útil: `"Payment validation failed: amount={amount} - {reason}"`

2. **Función `validate_payment(amount: float) -> float`**
   Debe validar:
   - `amount > 0` → Si no, levanta `PaymentError`
   - `amount <= 10000` → Si excede, levanta `PaymentError`
   - Si es válido, retorna el monto

3. **Función `process_payment(amount: float) -> str`**
   - Intenta validar usando `validate_payment()`
   - Si falla, captura la excepción y retorna: `"Payment failed: {error.reason}"`
   - Si tiene éxito, retorna: `"Payment processed: ${amount}"`

## Restricciones

- Las excepciones deben incluir contexto (no solo mensajes genéricos)
- Usa type hints en todos los parámetros y retornos
- Captura las excepciones correctamente en `process_payment()`

## Ejemplo de Uso

```python
print(process_payment(100))      # Payment processed: $100
print(process_payment(-50))      # Payment failed: amount must be positive
print(process_payment(15000))    # Payment failed: amount exceeds maximum
print(process_payment("abc"))    # (TypeError - no se valida este caso)
```
