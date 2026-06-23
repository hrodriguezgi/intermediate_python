def categorize_inventory(products: list[dict]) -> dict:
    """
    Organize inventory by category with detailed stats.

    Each product dict has: name, category, stock, active (bool).
    Return a dict with:
        - "categories": dict mapping category name to a dict with:
            - "products": list of product names (active only)
            - "total_stock": total stock in category (active only)
            - "count": number of active products
        - "summary": dict with:
            - "total_products": total active products
            - "total_stock": total active stock
            - "inactive_count": count of inactive products
            - "stock_by_category": dict mapping category to its total stock
    """
    categories = {}
    inactive_count = 0
    total_stock = 0

    for product in products:
        category = product["category"]
        is_active = product.get("active", True)

        if not is_active:
            inactive_count += 1
            continue

        if category not in categories:
            categories[category] = {
                "products": [],
                "total_stock": 0,
                "count": 0,
            }

        categories[category]["products"].append(product["name"])
        categories[category]["total_stock"] += product["stock"]
        categories[category]["count"] += 1
        total_stock += product["stock"]

    stock_by_category = {cat: data["total_stock"] for cat, data in categories.items()}

    return {
        "categories": categories,
        "summary": {
            "total_products": sum(data["count"] for data in categories.values()),
            "total_stock": total_stock,
            "inactive_count": inactive_count,
            "stock_by_category": stock_by_category,
        },
    }


if __name__ == "__main__":
    sample = [
        {"name": "Keyboard", "category": "hardware", "stock": 12, "active": True},
        {"name": "Mouse", "category": "hardware", "stock": 8, "active": True},
        {"name": "Broken Monitor", "category": "hardware", "stock": 2, "active": False},
        {"name": "Python Course", "category": "digital", "stock": 100, "active": True},
        {"name": "SQL Course", "category": "digital", "stock": 50, "active": True},
        {"name": "Deprecated Guide", "category": "digital", "stock": 1, "active": False},
    ]
    result = categorize_inventory(sample)
    print(result)
