def to_floats(values: list[str]) -> list[float]:
    return [float(value) for value in values]


def add_tax(values: list[float], tax_rate: float) -> list[float]:
    return [round(value * (1 + tax_rate), 2) for value in values]


def build_price_pipeline(values: list[str], tax_rate: float) -> list[float]:
    numeric_values = to_floats(values)
    return add_tax(numeric_values, tax_rate)


if __name__ == "__main__":
    print(build_price_pipeline(["10", "15.5", "20"], 0.19))
