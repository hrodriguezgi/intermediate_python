class PaymentValidationError(Exception):
    pass


def validate_payment(amount: float) -> float:
    if amount <= 0:
        raise PaymentValidationError("amount must be positive")
    return amount


if __name__ == "__main__":
    print(validate_payment(99.9))
