class PaymentError(ValueError):
    """Excepción personalizada para errores de pago con contexto."""

    def __init__(self, amount: float, reason: str) -> None:
        self.amount = amount
        self.reason = reason
        message = f"Payment validation failed: amount={amount} - {reason}"
        super().__init__(message)


def validate_payment(amount: float) -> float:
    """Valida que el monto de pago sea válido.

    Validaciones:
    - amount > 0
    - amount <= 10000

    Retorna el monto si es válido.
    Levanta PaymentError si no es válido.
    """
    # TODO: Implementa validación
    # Si amount <= 0: levanta PaymentError(amount, "amount must be positive")
    # Si amount > 10000: levanta PaymentError(amount, "amount exceeds maximum of $10000")
    # Si válido: retorna amount
    pass


def process_payment(amount: float) -> str:
    """Procesa un pago con manejo de errores.

    Intenta validar el pago. Si es válido, retorna mensaje de éxito.
    Si falla, retorna mensaje de error con la razón.
    """
    # TODO: Implementa con try/except
    # Captura PaymentError y retorna "Payment failed: {error.reason}"
    # Si tiene éxito, retorna "Payment processed: ${amount}"
    pass


if __name__ == "__main__":
    print(process_payment(100))      # Payment processed: $100
    print(process_payment(-50))      # Payment failed: amount must be positive
    print(process_payment(15000))    # Payment failed: amount exceeds maximum of $10000
    print(process_payment(5000))     # Payment processed: $5000
