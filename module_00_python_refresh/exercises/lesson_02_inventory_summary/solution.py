def build_inventory_summary(products: list[dict]) -> dict:
    """
    Build an inventory summary from a list of products.

    Each product dict has: name, category, stock.
    Return a dict with:
        - "total_products": number of products
        - "total_stock": total quantity across all products
        - "categories": sorted list of unique categories
        - "by_category": dict mapping category to total stock in that category
    """
    categories_set = set()
    total_stock = 0
    by_category = {}

    for product in products:
        category = product["category"]
        stock = product["stock"]

        categories_set.add(category)
        total_stock += stock

        if category not in by_category:
            by_category[category] = 0
        by_category[category] += stock

    return {
        "total_products": len(products),
        "total_stock": total_stock,
        "categories": sorted(categories_set),
        "by_category": by_category,
    }


if __name__ == "__main__":
    sample = [
        {"name": "Keyboard", "category": "hardware", "stock": 12},
        {"name": "Mouse", "category": "hardware", "stock": 8},
        {"name": "Monitor", "category": "hardware", "stock": 5},
        {"name": "Python Course", "category": "digital", "stock": 100},
        {"name": "SQL Course", "category": "digital", "stock": 50},
        {"name": "Design Book", "category": "books", "stock": 3},
    ]
    result = build_inventory_summary(sample)
    print(result)
