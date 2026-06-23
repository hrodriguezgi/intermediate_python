# Intermediate Python Course - Module Improvement Plan

> A data engineer's perspective on improving course content for technical students with real-world patterns and edge cases.

---

## Overview

This document outlines improvements for each module, organized by priority and implementation complexity. Each section includes:
- Current state
- Real-world gaps
- Specific recommendations with examples
- Suggested implementation approach

**Use this guide to create focused improvement sessions per module.**

---

## Module 0 · Python Refresh

### Current State
✅ Covers types, variables, truthy/falsy, basic data structures, simple queue/stack.

### Real-World Gaps

#### 1. **Data Structure Performance Trade-offs** (HIGH PRIORITY)
Students pick the wrong structure because they don't understand performance implications.

**The Problem:**
```python
# Both work, but one is 1000x slower for large datasets
large_list = list(range(1000000))
large_set = set(range(1000000))

# Check membership
"500000" in large_list   # O(n) - very slow with millions
500000 in large_set      # O(1) - instant
```

**Real-world scenario:** ETL pipeline processing 10M records, checking if ID exists:
- Using list + `in` → minutes
- Using set + `in` → milliseconds

**What to add:**
- Section: "Choosing the right structure"
  - `list` for ordered, mutating data
  - `tuple` for immutable, hashable data (can go in sets/dicts)
  - `dict` for labeled lookups
  - `set` for membership testing and deduplication (O(1) lookup)
- Show performance comparison with `timeit`
- Real scenario: deduplicating million-row CSV using set vs list

#### 2. **None vs Empty Containers** (MEDIUM PRIORITY)
Students conflate `None` with empty containers, causing bugs in data validation.

**The Problem:**
```python
def process_data(values):
    if values:  # False for [] AND None, but behavior should differ
        return sum(values)

process_data([])    # Probably want: return 0
process_data(None)  # Probably want: raise ValueError or return None

# Real mistake in data pipelines:
if response_data:  # Catches both empty dict AND missing API response
    process(response_data)
```

**What to add:**
- Section: "None is not empty"
  - Show explicit checks: `if values is None` vs `if not values`
  - When None means "not computed yet" vs "no data"
  - Example: Configuration system where `None` = "use default", `[]` = "disabled"

#### 3. **Mixed-Type Collections Gotcha** (MEDIUM PRIORITY)
Real data (APIs, CSVs, logs) is messy with mixed types. Students aren't prepared.

**The Problem:**
```python
# Real CSV data or API response
row = [1, "2", None, 3.5, True]

# Student code assumes all ints
total = sum(row)  # TypeError: unsupported operand type(s) for +: 'int' and 'str'

# Real scenario: JSON from API
data = {
    "id": 1,
    "count": "10",  # Was supposed to be int
    "tags": None,   # Was supposed to be list
    "active": "yes" # Was supposed to be bool
}
```

**What to add:**
- Section: "Real data is messy"
  - Example: Mixed-type list from CSV
  - Defensive conversion: `int(value) if value else 0`
  - Type checking patterns: `isinstance(value, int)`
  - How to handle validation errors

### Implementation Approach
- Add section after "Truthy y falsy" on structure choice
- Add "None vs empty" section before the None section
- Add "Real data messiness" subsection at the end with practical examples
- Include timing comparisons and real CSV data examples

---

## Module 1 · Pythonic Foundations

### Current State
✅ Data model, mutability, unpacking, enumerate, zip, dict merge are solid.

### Real-World Gaps

#### 1. **Shallow Copy Trap** (HIGH PRIORITY - Critical for data pipelines)
THE most common bug causing data mutations in shared collections.

**The Problem:**
```python
# Student code (think they have copies)
original = [["name", "Ana"], ["age", 30]]
copy = list(original)  # Shallow copy - inner lists still shared!

copy[0].append("NEW")  # Modifies BOTH lists
print(original)  # [["name", "Ana", "NEW"], ["age", 30]]

# Real impact in data pipelines:
users = [{"id": 1, "tags": []}, {"id": 2, "tags": []}]
users_copy = users.copy()  # Think they're independent
users_copy[0]["tags"].append("admin")  # Affects original too!
```

**Why it matters:** ETL processes often cache/backup data. Shallow copies fail silently.

**What to add:**
- Subsection: "Shallow copy gotcha" in mutability section
  - Show the nested list example
  - Explain `list()` and `dict.copy()` only copy top level
  - Show `copy.deepcopy()` solution
  - Real scenario: working with API responses that contain nested objects
  - When you actually need deepcopy vs when shallow copy is fine

#### 2. **Mutable Defaults in Dataclasses** (MEDIUM PRIORITY)
Footgun that bites every Python programmer at least once.

**The Problem:**
```python
from dataclasses import dataclass

@dataclass
class Config:
    tags: list = []  # WRONG: shared across all instances!
    settings: dict = {}

config1 = Config()
config1.tags.append("admin")

config2 = Config()
print(config2.tags)  # ["admin"] - BOTH share the same list!
```

**What to add:**
- Subsection in dataclasses section: "Mutable defaults"
  - Show the wrong way and why it fails
  - Correct way: use `field(default_factory=list)`
  - Explain `default_factory` is called for each instance
  - Real scenario: Configuration objects in data pipelines

#### 3. **Dict Ordering Guarantees Matter** (LOW PRIORITY - Nice to know)
Python 3.7+ dict ordering is predictable. Students should know this.

**The Problem:**
```python
# This NOW works consistently (Python 3.7+)
config = {"database": "prod", "timeout": 30}
later_config = {"timeout": 60, "region": "us"}

merged = {**config, **later_config}
print(merged)  # Order preserved, later values override

# But students don't realize:
# - Order matters for configuration precedence
# - Different Python versions behaved differently
```

**What to add:**
- Note when you show dict merging: mention order guarantee
- Show how later keys override: `{**defaults, **user_config}`
- Why this matters: predictable configuration merging

### Implementation Approach
- Add "Shallow Copy Trap" section right after current shallow copy section
- Add "Mutable Defaults" subsection in dataclass section
- Add note about dict ordering in the dict merge section

---

## Module 2 · Control Flow & Comprehensions

### Current State
✅ Basic control flow, comprehensions, generators covered.

### Real-World Gaps

#### 1. **Walrus Operator (`:=`)** (MEDIUM PRIORITY)
Modern Python feature (3.8+) that's super useful in data validation loops.

**The Problem:**
```python
# Without walrus operator (tedious)
while True:
    line = file.readline()
    if not line:
        break
    process(line)

# With walrus operator (elegant)
while (line := file.readline()):
    process(line)

# Real scenario: processing logs
while (event := queue.get()):
    if event is None:
        break
    process(event)
```

**What to add:**
- New section: "Walrus operator for validation loops"
  - Show log processing example
  - Show data validation in loops
  - Explain readability improvement
  - When to use vs regular assignment

#### 2. **Guard Clauses** (MEDIUM PRIORITY)
Escape "pyramid of doom" from nested conditions.

**The Problem:**
```python
# Bad: pyramid (hard to read, deep nesting)
def validate_and_process(user):
    if user is not None:
        if user.active:
            if user.has_permissions:
                if not user.is_banned:
                    return process(user)
    return None

# Good: guards (flat, readable)
def validate_and_process(user):
    if user is None:
        return None
    if not user.active:
        return None
    if not user.has_permissions:
        return None
    if user.is_banned:
        return None
    return process(user)
```

**Real scenario:** Data validation in ETL - checking multiple conditions before processing.

**What to add:**
- New section: "Guard clauses"
  - Show pyramid vs guards pattern
  - Explain early returns reduce cognitive load
  - Real scenario: validating CSV rows
  - Data processing pattern

#### 3. **Match Statements (Python 3.10+)** (HIGH PRIORITY)
Pattern matching for type-based logic. You're on 3.12, use it.

**The Problem:**
```python
# Without match (verbose)
if event_type == "payment":
    amount = event.get("amount")
    if isinstance(amount, (int, float)):
        process_payment(amount)
elif event_type == "refund":
    # ...
else:
    raise ValueError(f"Unknown event: {event_type}")

# With match (expressive)
match event:
    case {"type": "payment", "amount": int(amt) | float(amt)}:
        process_payment(amt)
    case {"type": "refund", "amount": int(amt) | float(amt)}:
        process_refund(amt)
    case {"type": "transfer", **rest}:
        process_transfer(rest)
    case _:
        raise ValueError(f"Unknown event type")
```

**Real scenario:** Parsing and validating API events or message queue data.

**What to add:**
- New section: "Pattern matching with match statements"
  - Show event processing example
  - Show extraction and type validation
  - Show catching unknown cases
  - Real scenario: message queue processing
  - Comparison to if/elif chains

### Implementation Approach
- Add walrus operator section in validation/loop section
- Add guard clauses section in control flow section
- Add match statements as new subsection
- Include practical data validation examples

---

## Module 3 · Functions & Decorators

### Current State
✅ Pure functions, decorators covered. Missing practical patterns for data processing.

### Real-World Gaps

#### 1. **Generator Expressions vs List Comprehensions** (HIGH PRIORITY - Critical for data)
Memory efficiency matters when processing GBs of data.

**The Problem:**
```python
# List comprehension: loads everything into memory
results = [expensive_transform(x) for x in huge_dataset]
# If huge_dataset has 1 billion rows: need GB of RAM

# Generator expression: lazy evaluation
results = (expensive_transform(x) for x in huge_dataset)
# Only transforms 1 row at a time, constant memory

# Real scenario: processing 100GB CSV
with open("huge.csv") as f:
    reader = csv.DictReader(f)
    
    # BAD: loads all 100GB into memory
    records = [transform(row) for row in reader]
    
    # GOOD: processes row by row
    records = (transform(row) for row in reader)
    for record in records:
        save_to_db(record)  # 1 row at a time
```

**What to add:**
- New section: "Generators for memory efficiency"
  - Show comprehension vs generator syntax
  - Explain lazy evaluation
  - Show memory impact with large datasets
  - Real scenario: streaming CSV processing
  - When to use each (small data = list, large data = generator)

#### 2. **Practical Decorators for Logging/Timing** (MEDIUM PRIORITY)
Your `traced` decorator is example-ish. Show real patterns.

**The Problem:**
```python
# Your current example (good for learning)
@traced
def compute_discount(total: float, rate: float) -> float:
    return round(total * (1 - rate), 2)

# Real-world: need timing and logging
@timing
def load_data(path: str) -> list[dict]:
    # How long does this take?
    pass

@log_calls
def validate_record(record: dict) -> bool:
    # What values are being validated?
    pass
```

**What to add:**
- Subsection: "Real decorators for data work"
  - `@timing`: measure execution time
    ```python
    def timing(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"{func.__name__} took {elapsed:.2f}s")
            return result
        return wrapper
    ```
  - `@log_calls`: log inputs/outputs
  - Real scenarios: ETL performance tracking

#### 3. **Partial Functions for Pipelines** (MEDIUM PRIORITY)
Useful for configuration and reusable transformations.

**The Problem:**
```python
from functools import partial

# Without partial: need wrapper functions
def normalize_score_100(score):
    return normalize_score(score, max_score=100)

def normalize_score_200(score):
    return normalize_score(score, max_score=200)

# With partial: elegant
normalize_100 = partial(normalize_score, max_score=100)
normalize_200 = partial(normalize_score, max_score=200)

# Real scenario: data transformation pipeline
clean_names = partial(str.strip)
upper_names = partial(str.upper)

# Chain them
pipeline = [clean_names, upper_names]
result = reduce(lambda x, f: f(x), pipeline, "  HELLO  ")
```

**What to add:**
- New section: "Partial functions for pipelines"
  - Show configuration use case
  - Show transformation pipeline pattern
  - Real scenario: CSV column transformation

#### 4. **Default Mutable Arguments** (MEDIUM PRIORITY)
Same footgun as dataclasses, but in regular functions.

**The Problem:**
```python
def collect_data(new_item, cache=[]):  # WRONG!
    cache.append(new_item)
    return cache

collect_data("first")   # Returns ["first"]
collect_data("second")  # Returns ["first", "second"] - shared cache!

# Correct way
def collect_data(new_item, cache=None):
    if cache is None:
        cache = []
    cache.append(new_item)
    return cache
```

**What to add:**
- Note in *args/**kwargs section: "Never use mutable defaults"
  - Explain why it happens (function definition evaluated once)
  - Show real data collection scenario
  - Show correct pattern

### Implementation Approach
- Add generator expressions section (high visibility)
- Add practical decorators subsection
- Add partial functions section
- Add mutable defaults note in parameters section

---

## Module 4 · Files & Serialization

### Current State
⚠️ Covers pathlib, text I/O, CSV, JSON, pickle. Missing critical edge cases.

### Real-World Gaps

#### 1. **Encoding Edge Cases** (HIGH PRIORITY)
Real-world files are messy. UTF-8 assumes work.

**The Problem:**
```python
# Your current code
content = LOG_PATH.read_text(encoding="utf-8")

# Real problems:
# 1. Excel CSV has BOM (byte order mark)
with open("excel_export.csv", encoding="utf-8") as f:
    header = f.readline()  # First cell has weird character

# 2. Legacy system uses latin-1
data = LOG_PATH.read_text(encoding="utf-8")  # Crashes on non-ASCII

# 3. Mixed encodings in same file (shouldn't happen, but does)

# What to do
# Option 1: Handle BOM
content = LOG_PATH.read_text(encoding="utf-8-sig")

# Option 2: Detect encoding
import chardet
raw = LOG_PATH.read_bytes()
detected = chardet.detect(raw)
content = raw.decode(detected["encoding"])

# Option 3: Graceful fallback
try:
    content = LOG_PATH.read_text(encoding="utf-8")
except UnicodeDecodeError:
    content = LOG_PATH.read_text(encoding="latin-1", errors="replace")
```

**What to add:**
- New subsection: "Encoding in the real world"
  - Show BOM problem with Excel CSVs
  - Show `utf-8-sig` encoding for Excel
  - Show legacy encoding issues
  - Show graceful fallback pattern
  - Mention `chardet` for auto-detection

#### 2. **Streaming Large Files** (HIGH PRIORITY - Critical for data)
You're loading entire files, which fails on big data.

**The Problem:**
```python
# Your current code
content = LOG_PATH.read_text()  # 10GB file → crashes

# Real scenario: process 100GB log file
for line in LOG_PATH.open(encoding="utf-8"):
    # Process one line at a time
    # Memory stays constant regardless of file size
    process(line.strip())

# CSV streaming
import csv
with open("huge.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Process one row, not entire file
        process_row(row)
```

**What to add:**
- New subsection: "Streaming large files"
  - Show memory problem with read_text()
  - Show line-by-line pattern
  - Show CSV DictReader (vs reading entire file)
  - Real scenario: processing multi-GB logs
  - Importance: "Why this matters for data engineering"

#### 3. **Context Managers (with statement)** (MEDIUM PRIORITY)
You use `with` but don't explain why it's critical.

**The Problem:**
```python
# Without context manager: file might not close
f = open("data.txt")
content = f.read()
# If exception happens here, file stays open
process(content)
f.close()  # Never reached if exception

# With context manager: file always closes
with open("data.txt") as f:
    content = f.read()
    process(content)
# File automatically closed, even if exception

# Same for Path
with LOG_PATH.open(encoding="utf-8") as f:
    for line in f:
        process(line)
```

**What to add:**
- Expand current `with` usage
- Section: "Why context managers matter"
  - Show exception safety
  - Show resource cleanup (file handles, DB connections)
  - Real scenario: processing aborted, files left open

#### 4. **TOML for Configuration** (LOW PRIORITY - Nice addition)
Modern Python has built-in TOML support. Better than JSON for configs.

**The Problem:**
```python
# JSON config (verbose, no comments)
{
  "database": "prod",
  "timeout": 30,
  "debug": false
}

# TOML config (readable, allows comments)
[database]
host = "prod"
timeout = 30
debug = false  # Easier to read

# Python 3.11+ has tomllib
import tomllib
config = tomllib.loads(path.read_text())
# Much nicer than json.loads
```

**What to add:**
- New subsection: "TOML for configuration files"
  - Show syntax
  - Show `tomllib` usage
  - When to use vs JSON/YAML
  - Real scenario: configuration management

#### 5. **CSV Dialect Edge Cases** (MEDIUM PRIORITY)
Real CSVs vary wildly. No guaranteed format.

**The Problem:**
```python
import csv

# Standard CSV
reader = csv.DictReader(f)

# Real-world variations
# - Semicolon separator (European Excel)
reader = csv.DictReader(f, delimiter=";")

# - Different quoting
reader = csv.DictReader(f, quotechar="'")

# - Different encoding + dialect
with open("file.csv", encoding="latin-1") as f:
    reader = csv.DictReader(f, delimiter=";", skipinitialspace=True)
    for row in reader:
        process(row)
```

**What to add:**
- Expand CSV section with:
  - Different delimiters (`;`, `\t`)
  - Encoding combined with CSV reading
  - Real scenario: importing from different sources

### Implementation Approach
- Add encoding subsection with BOM and fallback patterns
- Add streaming section (high priority - show generator pattern)
- Expand context manager explanation
- Add TOML section (quick addition)
- Expand CSV section with dialect variations

---

## Module 5 · OOP & Errors

### Current State
⚠️ Covers dataclasses, dunder methods, basic exceptions. Too shallow for production use.

### Real-World Gaps

#### 1. **Inheritance vs Composition** (MEDIUM PRIORITY)
You avoid inheritance (good!), but students need to understand both.

**The Problem:**
```python
# Inheritance (common mistake in data modeling)
class DataSource(ABC):
    def read(self): pass

class CSVSource(DataSource):
    def read(self): return read_csv()

class JSONSource(DataSource):
    def read(self): return read_json()

# Problem: if JSONSource also needs caching, now you have multiple inheritance mess

# Composition (better for data objects)
class DataReader:
    def __init__(self, source: DataSource, cache: Cache = None):
        self.source = source
        self.cache = cache
    
    def read(self):
        if self.cache and self.cache.has(id):
            return self.cache.get(id)
        data = self.source.read()
        if self.cache:
            self.cache.set(id, data)
        return data
```

**What to add:**
- New section: "Inheritance vs Composition"
  - Show inheritance anti-pattern
  - Show composition pattern
  - Real scenario: data source with caching
  - "Prefer composition for data objects"

#### 2. **Custom Exceptions with Context** (HIGH PRIORITY)
Basic exceptions don't communicate enough in data pipelines.

**The Problem:**
```python
# Your current approach (too generic)
class DataValidationError(ValueError):
    pass

# What happens in real code
try:
    validate_row(row_data)
except DataValidationError as e:
    print(e)  # "Invalid data" - not helpful, which field?

# Better: include context
class DataValidationError(ValueError):
    def __init__(self, field: str, value: any, reason: str):
        self.field = field
        self.value = value
        self.reason = reason
        super().__init__(
            f"Validation failed: {field}={value!r} - {reason}"
        )

# Real usage
try:
    if not isinstance(row["age"], int):
        raise DataValidationError(
            field="age",
            value=row["age"],
            reason="expected integer, got " + type(row["age"]).__name__
        )
except DataValidationError as e:
    print(f"Row {row_num}: {e}")
    print(f"  Field: {e.field}, Value: {e.value}")
```

**What to add:**
- New subsection: "Custom exceptions with context"
  - Show exception with metadata
  - Show real data validation scenario
  - How to include field names, values, reasons
  - Real scenario: CSV row processing with detailed error messages

#### 3. **Validation Errors vs Logic Errors** (MEDIUM PRIORITY)
Different errors should be raised for different problems.

**The Problem:**
```python
# All these use Exception, but different semantics

# Bad input (user/data error) → ValueError
if not isinstance(count, int):
    raise ValueError("count must be integer")

# Programming mistake (developer error) → TypeError
if callback is not None and not callable(callback):
    raise TypeError("callback must be callable")

# Domain logic violated (business logic error) → custom exception
if balance < amount:
    raise InsufficientFundsError(f"balance={balance}, amount={amount}")

# Should never happen (bug) → RuntimeError
if state not in ["open", "closed", "pending"]:
    raise RuntimeError(f"Invalid state: {state}")
```

**What to add:**
- New subsection: "Choosing the right exception"
  - `ValueError`: bad user input
  - `TypeError`: programmer mistake (wrong type)
  - Custom exceptions: domain logic violations
  - Real scenario: data processing pipeline errors

#### 4. **Protocol Types for Interfaces** (LOW PRIORITY - Advanced)
Pythonic way to define interfaces without inheritance.

**The Problem:**
```python
# Without Protocol: weird inheritance for interfaces
class DataLoader(ABC):
    @abstractmethod
    def load(self) -> dict: ...

# Everything must explicitly inherit from DataLoader
class CSVLoader(DataLoader):
    def load(self): return read_csv()

# With Protocol: structural subtyping (duck typing with type hints)
from typing import Protocol

class DataLoader(Protocol):
    def load(self) -> dict: ...

# Automatically "compatible" if it has load() method
class CSVLoader:
    def load(self) -> dict:
        return read_csv()  # Works with DataLoader type hint

# Real scenario: dependency injection
def process_data(loader: DataLoader):  # Accepts anything with load()
    data = loader.load()
    return transform(data)

process_data(CSVLoader())    # Works
process_data(DatabaseLoader()) # Works, no inheritance needed
```

**What to add:**
- Optional subsection: "Protocol types"
  - Show when to use vs inheritance/ABC
  - Real scenario: data source abstraction
  - Keep it brief - this is advanced

### Implementation Approach
- Add inheritance vs composition section
- Add custom exceptions with context (high priority)
- Add exception type guidance section
- Add Protocol types as optional advanced section

---

## Module 6 · Packages & SQLite

### Current State
⚠️ Covers package structure, SQLite intro. SQLite section is too brief for real use.

### Real-World Gaps

#### 1. **SQLite Limitations & When NOT to Use** (HIGH PRIORITY)
Never mentioned, but critical for production decisions.

**The Problem:**
```python
# SQLite is great for:
# - Single-user applications
# - Embedded databases
# - Data science notebooks
# - Testing (in-memory databases)

# SQLite is BAD for:
# - Multiple concurrent writers (only 1 writer at a time)
# - Network applications (it's a file, not a server)
# - High-concurrency situations (web apps with 100+ req/sec)
# - Complex queries with 100M+ rows (no query optimization)

# Real mistake:
# Web app with SQLite and uWSGI workers
# Multiple processes → writer lock contention → timeouts
```

**What to add:**
- New section: "When to use SQLite"
  - What SQLite is good for
  - Limitations clearly stated
  - When to use PostgreSQL/MySQL instead
  - Real scenario: migrating from SQLite to real DB

#### 2. **Parameterized Queries (SQL Injection Prevention)** (HIGH PRIORITY - Security)
SQL injection is real, even for SQLite.

**The Problem:**
```python
# WRONG: SQL injection vulnerability
user_id = "1; DROP TABLE users; --"
cursor.execute(f"SELECT * FROM users WHERE id={user_id}")

# RIGHT: parameterized queries
user_id = 1
cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))

# Real scenario: user input from web form
user_input = request.form.get("search")

# BAD
cursor.execute(f"SELECT * FROM products WHERE name LIKE '%{user_input}%'")

# GOOD
cursor.execute(
    "SELECT * FROM products WHERE name LIKE ?",
    (f"%{user_input}%",)
)
```

**What to add:**
- New subsection: "Parameterized queries"
  - Show SQL injection example
  - Explain why it matters
  - Show correct syntax (? for placeholders)
  - Real scenario: search form or filtering

#### 3. **Connection Management & Transactions** (HIGH PRIORITY)
Data integrity depends on proper transaction handling.

**The Problem:**
```python
# Current approach (probably missing context manager)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("INSERT INTO users ...")
conn.commit()

# Better: context manager
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users ...")
    # Auto-commits on success, rolls back on error

# Real scenario: multi-step process that must be atomic
with sqlite3.connect(db_path) as conn:
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions ...")
        cursor.execute("UPDATE accounts SET balance = balance - ?")
        # Both succeed or both fail (atomicity)
    except Exception:
        conn.rollback()  # Explicit rollback if needed
        raise
    conn.commit()  # Both statements committed together
```

**What to add:**
- New subsection: "Transactions for data safety"
  - Show context manager pattern
  - Explain atomicity (all-or-nothing)
  - Show multi-statement transactions
  - Real scenario: financial operations

#### 4. **Connection Pooling & Concurrency** (MEDIUM PRIORITY)
Real apps need efficient connection management.

**The Problem:**
```python
# Anti-pattern: create new connection for each query
def get_user(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return cursor.fetchone()

# Better: reuse connections (simplified for SQLite, but concept matters)
# For real DBs (PostgreSQL), use connection pooling
from psycopg2 import pool

db_pool = pool.SimpleConnectionPool(1, 20, database="mydb")

def get_user(user_id):
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return cursor.fetchone()
    finally:
        db_pool.putconn(conn)
```

**What to add:**
- Note: "Connection pooling concepts"
  - Why it matters for performance
  - How it works (brief)
  - Real scenario: migrating from SQLite to PostgreSQL
  - Show difference (SQLite minimal, PostgreSQL critical)

#### 5. **Error Handling in DB Operations** (MEDIUM PRIORITY)
DB operations have specific error patterns.

**The Problem:**
```python
# What happens?
cursor.execute("INSERT INTO users (email) VALUES (?)", (email,))
# Might fail with:
# - sqlite3.IntegrityError: UNIQUE constraint failed (duplicate)
# - sqlite3.OperationalError: no such table
# - sqlite3.ProgrammingError: syntax error

# Real code must handle these
try:
    cursor.execute("INSERT INTO users ...")
except sqlite3.IntegrityError as e:
    if "UNIQUE constraint" in str(e):
        raise DuplicateUserError(email)
    raise
except sqlite3.OperationalError as e:
    raise DatabaseError(f"Cannot access database: {e}")
```

**What to add:**
- Subsection: "Database error handling"
  - Common SQLite exceptions
  - How to distinguish errors
  - Real scenario: duplicate key handling in bulk insert

### Implementation Approach
- Add "When to use SQLite" section (high visibility)
- Add parameterized queries section (security)
- Add transactions subsection (critical)
- Add connection pooling note
- Add error handling subsection
- Significantly expand SQLite section

---

## Missing Topics (Consider as Future Modules)

### Module 7: Testing & Data Validation
**Why it matters:** Data engineers must validate transformations. No testing coverage in current course.

**Would cover:**
- `pytest` basics
- Testing data transformations
- Fixtures for test data
- Parameterized tests for edge cases
- Real scenario: validating ETL pipeline outputs

### Module 8: Logging & Debugging
**Why it matters:** Production data work requires visibility. `print()` is useless in production.

**Would cover:**
- `logging` module
- Log levels (debug, info, warning, error)
- Structured logging for data pipelines
- Integration with data processing
- Real scenario: tracking data quality issues

### Module 9: Type Hints Advanced
**Why it matters:** Type hints enable better data modeling and IDE support.

**Would cover:**
- `TypedDict` for structured data
- `Generic[T]` for type-safe containers
- `Union` vs `Optional`
- Protocol types deeper
- Real scenario: type-safe data validation

### Module 10: Virtual Environments & Dependency Management
**Why it matters:** Data projects have exact version requirements.

**Would cover:**
- `uv` setup (already used, but not explained)
- Why virtual environments matter
- Reproducible dependencies
- `pyproject.toml` configuration
- Real scenario: sharing reproducible pipelines

---

## Implementation Priority Matrix

| Priority | Module | Topic | Effort | Impact |
|----------|--------|-------|--------|--------|
| HIGH | 0 | Data structure performance | Low | High |
| HIGH | 1 | Shallow copy trap | Low | High |
| HIGH | 2 | Walrus operator | Low | Medium |
| HIGH | 2 | Match statements | Low | Medium |
| HIGH | 3 | Generators vs comprehensions | Medium | High |
| HIGH | 4 | Streaming large files | Low | High |
| HIGH | 5 | Custom exceptions with context | Medium | Medium |
| HIGH | 6 | SQL injection prevention | Low | High |
| HIGH | 6 | Transactions | Low | High |
| MEDIUM | 1 | Shallow copy deepcopy | Low | Medium |
| MEDIUM | 1 | Mutable defaults | Low | Medium |
| MEDIUM | 2 | Guard clauses | Low | Medium |
| MEDIUM | 3 | Practical decorators | Medium | Medium |
| MEDIUM | 4 | Encoding edge cases | Medium | Medium |
| MEDIUM | 5 | Inheritance vs composition | Medium | Medium |
| MEDIUM | 6 | SQLite limitations | Low | Medium |
| LOW | 1 | Dict ordering | Low | Low |
| LOW | 3 | Partial functions | Low | Low |
| LOW | 4 | TOML configuration | Low | Low |
| LOW | 5 | Protocol types | Medium | Low |
| LOW | 6 | Connection pooling | Low | Low |

---

## Suggested Session Organization

### Session 1: Module 0 Improvements
Focus on data structure performance and real data messiness.
Time: ~1 hour

### Session 2: Module 1 Improvements
Focus on shallow copy trap and mutable defaults.
Time: ~1 hour

### Session 3: Module 2 Improvements
Focus on walrus operator, guard clauses, and match statements.
Time: ~1.5 hours

### Session 4: Module 3 Improvements
Focus on generators and practical decorators.
Time: ~1 hour

### Session 5: Module 4 Improvements
Focus on streaming files, encoding, and CSV edge cases.
Time: ~1.5 hours

### Session 6: Module 5 Improvements
Focus on custom exceptions and error handling.
Time: ~1 hour

### Session 7: Module 6 Improvements
Focus on SQL injection, transactions, and SQLite limitations.
Time: ~1.5 hours

---

## Notes for Implementation

1. **Maintain course tone:** Keep Spanish explanations where appropriate, keep practical focus
2. **Include real examples:** Use data engineering scenarios (CSV processing, ETL, logging)
3. **Show the problem first:** Always show what goes wrong before showing the solution
4. **Include performance implications:** Data engineers care about speed and memory
5. **Test changes:** Run examples, ensure they work with Python 3.12
6. **Update exercises if needed:** Some exercises might need enhancement to cover new content

---

## Questions for Each Session

Before starting a session, ask yourself:
- What problem are students solving with this knowledge?
- Where does this fail in real data work?
- Can I show a performance/correctness comparison?
- Is there a real scenario (CSV processing, API parsing, etc.)?
