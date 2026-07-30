# Final Project: E-Commerce Inventory Management System

## Overview

You're building a complete data application for an e-commerce company that needs to:
1. **Ingest** product data from CSV files
2. **Validate** and transform the data
3. **Store** inventory in SQLite (transactional)
4. **Analyze** sales trends in DuckDB (analytical)
5. **Expose** everything via a FastAPI REST API

This project ties together all 7 modules of the course into a real-world scenario.

---

## Real-World Context

**Scenario:** Your company receives daily product updates from 5 different vendors. Each sends a CSV with products in different formats (inconsistent column names, encoding issues, mixed data types). 

You need a system that:
- Loads these CSVs reliably
- Validates product data
- Stores it persistently
- Allows fast queries
- Provides an API for the web team

**Timeline:** ~6 hours to complete (can be split across days)

---

## Project Phases

### Phase 1: Data Loading & Validation (1 hour)
**Modules used:** 0, 4

Load CSV files with proper error handling:
```
products.csv
├── id, name, category, price, stock
├── Handle encoding errors (UTF-8, Latin-1)
├── Handle missing values
└── Detect and fix data types
```

**File:** `01_data_loading.py`

**What you'll learn:**
- Streaming CSV without loading everything in memory
- Type inference and validation
- Error recovery

---

### Phase 2: Data Models (30 min)
**Modules used:** 5

Define ORM models and validation:
```
Product
├── id (int)
├── name (str)
├── price (float)
├── category (str)
├── stock (int)
└── created_at (datetime)
```

**File:** `02_database_models.py`

**What you'll learn:**
- SQLAlchemy ORM patterns
- Type-safe models
- Custom validation

---

### Phase 3: SQLite Integration (1 hour)
**Modules used:** 6

Persistent data storage with transactions:

**File:** `03_sqlite_operations.py`

**What you'll learn:**
- ACID transactions
- Bulk inserts with error handling
- Duplicate detection
- Atomic operations

---

### Phase 4: DuckDB Analytics (30 min)
**Modules used:** 6

Fast analytical queries on product data:

**File:** `04_duckdb_analytics.py`

Queries:
- Top 10 products by category
- Revenue by category
- Low-stock alerts
- Supplier performance

**What you'll learn:**
- Analytics SQL patterns
- Performance comparison
- Data export

---

### Phase 5: FastAPI Application (1.5 hours)
**Modules used:** 7

REST API with:
- **GET /products** - list products (with pagination, filtering)
- **GET /products/{id}** - get single product
- **POST /products** - add new product
- **PUT /products/{id}** - update product
- **DELETE /products/{id}** - remove product
- **GET /analytics** - inventory stats
- **POST /sales** - sell product (reduces stock)

**File:** `05_fastapi_application.py`

**What you'll learn:**
- Pydantic validation
- Database integration
- Error handling
- HTTP status codes

---

### Phase 6: Testing & Documentation (30 min)
**File:** `06_test_guide.md`

Test endpoints:
- Valid requests
- Invalid data (validation errors)
- Edge cases (duplicate names, negative prices)
- Not found (404)

---

## Learning Objectives

By the end, you'll understand:

| Module | Concept | Application |
|--------|---------|------------|
| **0** | Data structures | Choosing dict/set/list for performance |
| **1** | Pythonic patterns | Clean iteration and unpacking |
| **2** | Control flow | Validation guards and comprehensions |
| **3** | Functions & decorators | Reusable transformation pipeline |
| **4** | Files & serialization | Loading and parsing CSV reliably |
| **5** | OOP & errors | Models with validation and custom errors |
| **6** | Databases | SQLite transactions + DuckDB analytics |
| **7** | FastAPI | Building complete REST API |

---

## Project Structure

```
final_project/
├── 00_PROJECT_BRIEF.md            ← You are here
├── 01_data_loading.py             # Load & validate CSV
├── 02_database_models.py          # SQLAlchemy ORM
├── 03_sqlite_operations.py        # Insert & query SQLite
├── 04_duckdb_analytics.py         # Analytics queries
├── 05_fastapi_application.py      # Complete API
├── 06_test_guide.md               # How to test
├── data/
│   ├── products.csv               # Sample data
│   ├── inventory.db               # SQLite (auto-created)
│   ├── analytics.duckdb           # DuckDB (auto-created)
│   └── vendor_*.csv               # Multiple vendors
├── src/
│   ├── models.py                  # Shared ORM models
│   ├── schemas.py                 # Pydantic models
│   └── database.py                # Database connections
└── README.md                       # How to run
```

---

## Key Patterns You'll Use

### 1. Error Handling
```python
try:
    validate(data)
    store(data)
except ValidationError as e:
    log_error(e)
    continue  # Skip bad rows
```

### 2. Batch Processing
```python
for batch in chunks(rows, size=1000):
    insert_batch(db, batch)
    db.commit()
```

### 3. Transactions
```python
with Session(engine) as db:
    # Both statements or neither
    update_product(db, product_id, new_stock)
    record_sale(db, product_id, quantity)
    db.commit()
```

### 4. API Validation
```python
@app.post("/products")
async def create_product(product: ProductCreate):
    # Pydantic validates automatically
    # FastAPI gives 422 if invalid
```

---

## Success Criteria

 **Phase 1:** Load 100+ rows from CSV without crashing
 **Phase 2:** Models compile without errors
 **Phase 3:** Bulk insert with transaction handling
 **Phase 4:** Analytical queries execute fast (< 100ms)
 **Phase 5:** All endpoints work in Swagger UI
 **Phase 6:** Can test with curl/Postman

---

## Time Breakdown

| Phase | Time | Complexity |
|-------|------|-----------|
| 1: Data Loading | 1h | Medium |
| 2: Models | 30min | Low |
| 3: SQLite | 1h | Medium |
| 4: DuckDB | 30min | Low |
| 5: FastAPI | 1.5h | High |
| 6: Testing | 30min | Low |
| **Total** | **5-6h** | - |

---

## Starting Point

Each phase has:
1. **Learning objectives** - what you'll understand
2. **Skeleton code** - basic structure
3. **TODO comments** - what to implement
4. **Test cases** - verify it works

You'll fill in the TODOs and run tests to verify.

---

## Troubleshooting

**CSV not loading?**
- Check encoding (UTF-8, Latin-1, or UTF-8-sig)
- Check file exists and is readable
- Print first few rows to debug

**Database won't open?**
- Check path exists
- Try deleting old .db file
- Check SQL syntax

**API won't start?**
- Check imports (all dependencies installed)
- Check port 8000 is free
- Check model definitions are complete

**Validation failing?**
- Print the error details
- Check Pydantic model matches data
- Add example data

---

## Tips

1. **Start with Phase 1** - get data loading working first
2. **Test each phase independently** - don't wait for the API to test models
3. **Use print() liberally** - debug by printing intermediate steps
4. **Check SQL manually** - write query in DuckDB CLI first
5. **Use Swagger UI** - test API visually before curl

---

## Going Deeper (Optional)

After completing the project, consider:

- Add logging (Module 8 - if you get there)
- Add user authentication (FastAPI feature)
- Add async/await for performance
- Deploy to cloud (AWS, Heroku, etc.)
- Add tests (pytest)
- Add CI/CD pipeline

---

**Ready?** Start with **01_data_loading.py** 
