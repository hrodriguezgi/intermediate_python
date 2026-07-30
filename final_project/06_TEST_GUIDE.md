# Testing Guide

## Testing Each Phase

### Phase 1: Data Loading
```bash
python 01_data_loading.py
```

Should output:
```
Loading data from .../products.csv...
✓ Loaded 20 products
Total products: 20
Categories: Electronics, Accessories, Furniture, Lighting
Price range: $7.99 - $1299.99
Total stock: 3,085 units
Low stock products: 0

First 3 products:
  {'id': 1, 'name': 'Professional Laptop', ...}
  ...
```

---

### Phase 2: Database Models
```bash
python 02_database_models.py
```

Should output:
```
Database initialized: .../inventory.db
Database schema created successfully!
Database file: .../inventory.db
```

Check that file `data/inventory.db` exists.

---

### Phase 3: SQLite Operations
```bash
python 03_sqlite_operations.py
```

Should output:
```
Loading products from CSV...
✓ Loaded 20 products

Inserting into SQLite...
Inserted 20 products (0 failed)

Verifying data...
Total in database: 20

Testing operations...
✓ Product 1: Professional Laptop - $1299.99 (15 in stock)
✓ Updated stock to 12
✓ Sold 2 units, new stock: 13
```

---

### Phase 4: DuckDB Analytics
```bash
python 04_duckdb_analytics.py
```

Should output:
```
Initializing analytics engine...
Loading products from .../products.csv...

============================================================
INVENTORY ANALYTICS REPORT
============================================================

Category Statistics:
  Electronics: 6 products, $3,087.92, avg $514.65
  Accessories: 7 products, $2,659.92, avg $37.99
  ...

Low Stock Alert (< 20):
  None

Total Inventory Value: $52,345.92

Analytics complete!
```

---

### Phase 5: FastAPI Application

#### Start Server
```bash
uvicorn 05_fastapi_application:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Test in Browser/Swagger UI
Visit: `http://localhost:8000/docs`

You'll see interactive API documentation.

---

## Testing Endpoints with curl

### GET: List products
```bash
curl http://localhost:8000/products
```

Response:
```json
[
  {
    "id": 1,
    "name": "Professional Laptop",
    "category": "Electronics",
    "price": 1299.99,
    "stock": 15,
    "created_at": "2024-01-01T00:00:00"
  },
  ...
]
```

### GET: Single product
```bash
curl http://localhost:8000/products/1
```

### GET: With filters
```bash
curl "http://localhost:8000/products?category=Electronics&skip=0&limit=5"
```

### POST: Create product
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Product",
    "price": 99.99,
    "category": "Electronics",
    "stock": 50
  }'
```

Response (201 Created):
```json
{
  "id": 21,
  "name": "New Product",
  "price": 99.99,
  "category": "Electronics",
  "stock": 50,
  "created_at": "2024-01-15T10:30:45"
}
```

### PUT: Update product
```bash
curl -X PUT http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "stock": 12
  }'
```

### DELETE: Delete product
```bash
curl -X DELETE http://localhost:8000/products/21
```

### POST: Record sale
```bash
curl -X POST http://localhost:8000/sales \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

Response:
```json
{
  "product_name": "Professional Laptop",
  "quantity_sold": 2,
  "new_stock": 13,
  "total_price": 2599.98
}
```

### GET: Analytics summary
```bash
curl http://localhost:8000/analytics/summary
```

Response:
```json
{
  "total_products": 20,
  "total_value": 52345.92,
  "average_price": 187.43,
  "low_stock_count": 0
}
```

---

## Testing Edge Cases

### Test: Duplicate product (should fail)
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Professional Laptop",
    "price": 999.99,
    "category": "Electronics",
    "stock": 10
  }'
```

Expected: 400 error - "Product 'Professional Laptop' already exists"

### Test: Negative price (should fail)
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "price": -99.99,
    "category": "Electronics"
  }'
```

Expected: 422 validation error - "ensure this value is greater than 0"

### Test: Insufficient stock (should fail)
```bash
curl -X POST http://localhost:8000/sales \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 10000
  }'
```

Expected: 400 error - "Insufficient stock"

### Test: Product not found (404)
```bash
curl http://localhost:8000/products/99999
```

Expected: 404 error - "Product 99999 not found"

---

## Using Postman

Import this collection into Postman:

```json
{
  "info": {
    "name": "Inventory API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "List Products",
      "request": {"method": "GET", "url": "http://localhost:8000/products"}
    },
    {
      "name": "Get Product",
      "request": {"method": "GET", "url": "http://localhost:8000/products/1"}
    },
    {
      "name": "Create Product",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/products",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {"mode": "raw", "raw": "..."}
      }
    }
  ]
}
```

---

## Debugging Tips

**Database won't open?**
- Delete `data/inventory.db` and re-run Phase 2

**API won't start?**
- Check all imports in 05_fastapi_application.py
- Check that port 8000 is free
- Run with `--reload` flag for development

**Data not showing?**
- Run Phase 3 first to populate database
- Check CSV file exists at `data/products.csv`

**Tests failing?**
- Print intermediate steps
- Check error messages
- Use Swagger UI for debugging

---

## Success Checklist

- [ ] Phase 1: CSV loads 20 products
- [ ] Phase 2: Database file created
- [ ] Phase 3: 20 products in database
- [ ] Phase 4: Analytics report displays
- [ ] Phase 5: API starts without errors
- [ ] GET /products returns data
- [ ] POST /products creates item
- [ ] PUT /products/{id} updates item
- [ ] DELETE /products/{id} removes item
- [ ] POST /sales updates stock
- [ ] GET /analytics/summary shows stats
- [ ] Swagger UI available at /docs

---

## Next Steps

After all tests pass:

1. Add more products via API
2. Generate sales and check stock updates
3. Monitor analytics changes
4. Try edge cases
5. Explore Swagger UI documentation

---
