def triage_orders(orders: list[dict]) -> dict:
    """Part 1: Basic classification with guard clauses."""
    summary = {"priority": [], "standard": [], "low_value": [], "blocked": []}

    for order in orders:
        if order["status"] != "paid":
            summary["blocked"].append(order["id"])
            continue
        if order["total"] >= 100:
            summary["priority"].append(order["id"])
        elif order["total"] >= 20:
            summary["standard"].append(order["id"])
        else:
            summary["low_value"].append(order["id"])

    return summary


def triage_orders_safe(orders: list[dict]) -> dict:
    """Part 2: Defensive validation for messy real-world data."""
    summary = {"priority": [], "standard": [], "low_value": [], "blocked": [], "invalid": []}

    for order in orders:
        # Validate required fields exist
        if "id" not in order or "total" not in order or "status" not in order:
            summary["invalid"].append(order.get("id"))
            continue

        # Convert total to number if it's a string
        try:
            total = float(order["total"]) if isinstance(order["total"], str) else order["total"]
        except (ValueError, TypeError):
            summary["invalid"].append(order["id"])
            continue

        # Classify using guard clauses
        status = order["status"]
        if status != "paid":
            summary["blocked"].append(order["id"])
        elif total >= 100:
            summary["priority"].append(order["id"])
        elif total >= 20:
            summary["standard"].append(order["id"])
        else:
            summary["low_value"].append(order["id"])

    return summary


def classify_order_match(order: dict) -> str:
    """Part 3: Use match statements for pattern-based classification."""
    match order:
        case {"status": "paid", "total": int(t) | float(t)} if t >= 100:
            return "priority"
        case {"status": "paid", "total": int(t) | float(t)} if t >= 20:
            return "standard"
        case {"status": "paid", "total": int(t) | float(t)}:
            return "low_value"
        case {"status": s} if s != "paid":
            return "blocked"
        case _:
            return "invalid"


if __name__ == "__main__":
    # Part 1: Basic example
    sample = [
        {"id": 1, "total": 150, "status": "paid"},
        {"id": 2, "total": 35, "status": "paid"},
        {"id": 3, "total": 8, "status": "paid"},
        {"id": 4, "total": 20, "status": "pending"},
    ]
    print("Part 1 - Basic triage:")
    print(triage_orders(sample))
    print()

    # Part 2: Messy data with validation
    messy = [
        {"id": 1, "total": 150, "status": "paid"},
        {"id": 2, "total": "35", "status": "paid"},  # String total
        {"id": 3},  # Missing fields
        {"id": 4, "total": 20, "status": None},  # Invalid status
        {"id": 5, "total": 75, "status": "paid"},
    ]
    print("Part 2 - Safe triage with validation:")
    print(triage_orders_safe(messy))
    print()

    # Part 3: Match statement classification
    print("Part 3 - Match statement classification:")
    for order in sample:
        category = classify_order_match(order)
        print(f"  Order {order['id']}: {category}")
