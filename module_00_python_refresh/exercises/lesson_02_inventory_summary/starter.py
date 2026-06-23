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
    pass


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
