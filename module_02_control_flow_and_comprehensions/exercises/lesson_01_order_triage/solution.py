def triage_orders(orders: list[dict]) -> dict:
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


if __name__ == "__main__":
    sample = [
        {"id": 1, "total": 150, "status": "paid"},
        {"id": 2, "total": 35, "status": "paid"},
        {"id": 3, "total": 8, "status": "paid"},
        {"id": 4, "total": 20, "status": "pending"},
    ]
    print(triage_orders(sample))
