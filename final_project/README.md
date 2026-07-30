# Final Project: E-Commerce Inventory Management System

Complete end-to-end data application using everything from the course.

## Quick Start

```bash
# Phase 1: Load and validate CSV
python 01_data_loading.py

# Phase 2: Create database models
python 02_database_models.py

# Phase 3: Insert data into SQLite
python 03_sqlite_operations.py

# Phase 4: Analytics with DuckDB
python 04_duckdb_analytics.py

# Phase 5: Start FastAPI server
uvicorn 05_fastapi_application:app --reload

# Then visit http://localhost:8000/docs
```

## Project Overview

**Goal:** Build a complete data application that:
1. Loads product data from CSV
2. Validates and transforms it
3. Stores in SQLite (transactional)
4. Analyzes with DuckDB (fast queries)
5. Exposes via REST API (FastAPI)

**Time:** ~5-6 hours (self-paced)

**Modules Used:** All 7 modules of the course

## Phases

### Phase 1: Data Loading (1 hour)
- Load CSV files
- Handle encoding errors
- Validate data types
- **File:** `01_data_loading.py`
- **Modules:** 0, 4

### Phase 2: Database Models (30 min)
- Define SQLAlchemy ORM
- Pydantic validation models
- Type-safe structures
- **File:** `02_database_models.py`
- **Modules:** 5

### Phase 3: SQLite Operations (1 hour)
- Bulk insert with transactions
- Error handling
- ACID guarantees
- **File:** `03_sqlite_operations.py`
- **Modules:** 6

### Phase 4: DuckDB Analytics (30 min)
- Analytical queries
- GROUP BY, aggregations
- Performance comparison
- **File:** `04_duckdb_analytics.py`
- **Modules:** 6

### Phase 5: FastAPI Application (1.5 hours)
- REST endpoints (GET, POST, PUT, DELETE)
- Database integration
- Pydantic validation
- **File:** `05_fastapi_application.py`
- **Modules:** 7

### Phase 6: Testing (30 min)
- Test all endpoints
- Edge cases
- Documentation
- **File:** `06_TEST_GUIDE.md`

## Project Structure

```
final_project/
├── 00_PROJECT_BRIEF.md          # This is the detailed brief
├── README.md                     # This file
├── 01_data_loading.py           # Phase 1: Load CSV
├── 02_database_models.py        # Phase 2: Define models
├── 03_sqlite_operations.py      # Phase 3: Database ops
├── 04_duckdb_analytics.py       # Phase 4: Analytics
├── 05_fastapi_application.py    # Phase 5: API
├── 06_TEST_GUIDE.md             # Phase 6: Testing
├── data/
│   ├── products.csv             # Sample data (20 products)
│   ├── inventory.db             # SQLite (auto-created)
│   └── analytics.duckdb         # DuckDB (auto-created)
└── src/
    ├── models.py                # Shared models
    ├── schemas.py               # Pydantic schemas
    └── database.py              # Database config
```

## Key Concepts

### Module 0: Data Structures
- Choosing `dict` for lookups
- `set` for deduplication
- Performance trade-offs

### Module 1: Pythonic Code
- Clean iteration
- Unpacking
- Mutability handling

### Module 2: Control Flow
- Guard clauses for validation
- Comprehensions for transforms
- Match statements (if using 3.10+)

### Module 3: Functions
- Transformation pipeline
- Decorators for timing
- Partial functions

### Module 4: Files & Serialization
- CSV loading with encoding
- Error recovery
- Streaming large files

### Module 5: OOP & Errors
- Model classes
- Custom exceptions
- Dataclass patterns

### Module 6: Databases
- SQLite for transactions
- DuckDB for analytics
- ORM patterns with SQLAlchemy

### Module 7: FastAPI
- REST endpoints
- Pydantic validation
- Error handling

## Requirements

```
Python 3.12+
SQLAlchemy>=2.0
FastAPI>=0.100
Uvicorn>=0.24
DuckDB>=0.8
Pydantic>=2.0
```

Install with:
```bash
pip install sqlalchemy fastapi uvicorn duckdb pydantic
```

Or using UV (recommended):
```bash
uv sync
```

## API Endpoints

### Products
- `GET /products` - List products
- `GET /products/{id}` - Get product
- `POST /products` - Create
- `PUT /products/{id}` - Update
- `DELETE /products/{id}` - Delete

### Sales
- `POST /sales` - Record sale

### Analytics
- `GET /analytics/summary` - Inventory stats

### Health
- `GET /health` - Health check
- `GET /` - Welcome

## Interactive Testing

Visit `http://localhost:8000/docs` for Swagger UI with interactive testing.

Or use curl:
```bash
# List products
curl http://localhost:8000/products

# Get one product
curl http://localhost:8000/products/1

# Create product
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":99.99,"category":"Electronics"}'

# Record sale
curl -X POST http://localhost:8000/sales \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"quantity":2}'
```

## Debugging

**CSV not loading?**
- Check file exists: `ls data/products.csv`
- Check encoding: file should be UTF-8
- Print first row: add `print(rows[0])`

**Database error?**
- Delete old database: `rm data/inventory.db`
- Re-run Phase 2 to recreate

**API won't start?**
- Check imports in Phase 5
- Check port 8000 is free: `lsof -i :8000`
- Run with `--reload`: `uvicorn 05_fastapi_application:app --reload`

**Validation failing?**
- Print the error message
- Check Pydantic model matches data
- Use Swagger UI to see schema

## Next Steps

1. **Complete all phases** - Each takes 30min-1.5h
2. **Test thoroughly** - Use `06_TEST_GUIDE.md`
3. **Explore variations** - Add new products, test limits
4. **Go deeper** - Add logging, tests, CI/CD

## Success Indicators

✅ CSV loads 20 products
✅ Database file created with schema
✅ SQLite populated with data
✅ DuckDB analytics run successfully
✅ FastAPI starts without errors
✅ All CRUD endpoints work
✅ Swagger UI displays correctly
✅ Can test with curl/Postman

## Learning Outcomes

After completing this project, you'll be able to:

- ✅ Build a complete data application from files to API
- ✅ Load, validate, and transform CSV data
- ✅ Use SQLite for transactional data
- ✅ Use DuckDB for analytical queries
- ✅ Create REST APIs with FastAPI
- ✅ Implement proper error handling
- ✅ Write type-safe Python code
- ✅ Apply every module in practice

## Optional Enhancements

After completing:

1. **Add authentication** - FastAPI security
2. **Add logging** - Track operations
3. **Add tests** - pytest for coverage
4. **Deploy** - AWS Lambda, Railway, Heroku
5. **Add caching** - Redis for performance
6. **Add async/await** - For performance
7. **Add pagination** - For large datasets

## Questions?

Refer to:
- `00_PROJECT_BRIEF.md` for detailed overview
- `06_TEST_GUIDE.md` for testing help
- Module lesson files for concepts
- Swagger UI at `/docs` for API schema

---

**Start with Phase 1:** `python 01_data_loading.py`
