# %% [markdown]
# # 02. SQLite con SQLAlchemy
#
# ## Objetivos
#
# - Usar SQLite con SQLAlchemy en aplicaciones reales
# - Manejar transacciones (ACID: Atomic, Consistent, Isolated, Durable)
# - Prevenir SQL injection con ORM
# - Manejar errores de base de datos
# - Entender cuándo usar SQLite vs otras bases de datos

# %% [markdown]
# ## Cuándo usar SQLite
#
# ###  Bueno para:
# - Aplicaciones de usuario único (editor de notas, desktop app)
# - Bases de datos embedded (datos en un archivo local)
# - Desarrollo y testing
# - Ciencia de datos (notebooks locales)
# - SQLite requiere 0 configuración de servidor
#
# ###  No es bueno para:
# - Aplicaciones web con múltiples usuarios concurrentes
# - Solo permite 1 escritor a la vez (lock de base de datos)
# - No es una base de datos de red (no es cliente-servidor)
# - Millones de filas con queries complejas (sin optimización)
#
# **Regla:** Si más de 1 proceso escribe simultáneamente, usa PostgreSQL/MySQL.

# %%
from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, declarative_base, relationship

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "orders.db"
DB_URL = f"sqlite:///{DB_PATH}"

Base = declarative_base()


# %% [markdown]
# ## Modelos con relaciones
#
# SQLAlchemy gestiona relaciones entre tablas automáticamente.


# %%
class Customer(Base):
    __tablename__ = "customers"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False, unique=True)
    email: str = Column(String(100), nullable=False, unique=True)
    balance: float = Column(Float, default=0.0)

    orders = relationship("Order", back_populates="customer")

    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, name='{self.name}', balance=${self.balance:.2f})>"


class Order(Base):
    __tablename__ = "orders"

    id: int = Column(Integer, primary_key=True)
    customer_id: int = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount: float = Column(Float, nullable=False)
    status: str = Column(String(20), default="pending")
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, customer_id={self.customer_id}, amount=${self.amount:.2f})>"


# %%
engine = create_engine(DB_URL, echo=False)
Base.metadata.create_all(engine)

print(f"Database created: {DB_PATH.exists()}")

# %% [markdown]
# ## Transacciones: Todo o Nada
#
# Una transacción es una serie de operaciones que deben completarse juntas.
# Si algo falla, todo se revierte (rollback).
#
# **Caso real:** Transferencia de dinero
# - Restar dinero de cuenta A
# - Sumar dinero a cuenta B
# - Si algo falla en el medio, ambas operaciones se revierten


# %%
def transfer_money(session: Session, from_id: int, to_id: int, amount: float):
    try:
        # Paso 1: Restar de la cuenta origen
        from_customer = session.query(Customer).filter(Customer.id == from_id).first()
        if not from_customer:
            raise ValueError(f"Customer {from_id} not found")

        if from_customer.balance < amount:
            raise ValueError(f"Insufficient funds. Balance: ${from_customer.balance}")

        from_customer.balance -= amount

        # Paso 2: Sumar a la cuenta destino
        to_customer = session.query(Customer).filter(Customer.id == to_id).first()
        if not to_customer:
            raise ValueError(f"Customer {to_id} not found")

        to_customer.balance += amount

        # Si llegamos aquí, todo es válido. Commit hace ambas operaciones permanentes.
        session.commit()
        print(f"Transfer successful: ${amount} from {from_customer.name} to {to_customer.name}")

    except ValueError as e:
        # Error de negocio: rollback automático en context manager
        print(f"Transfer failed: {e}")
        raise


# %%
# Setup: crear clientes
with Session(engine) as session:
    customers = [
        Customer(name="Ana", email="ana@example.com", balance=500.0),
        Customer(name="Bob", email="bob@example.com", balance=200.0),
    ]
    session.add_all(customers)
    session.commit()
    print("Customers created")

# %%
# Context manager: automáticamente commit() o rollback()
with Session(engine) as session:
    transfer_money(session, from_id=1, to_id=2, amount=100.0)

# Verificar que el cambio se guardó
with Session(engine) as session:
    ana = session.query(Customer).filter(Customer.name == "Ana").first()
    bob = session.query(Customer).filter(Customer.name == "Bob").first()
    print(f"\nAfter transfer:")
    print(f"  Ana: ${ana.balance:.2f}")
    print(f"  Bob: ${bob.balance:.2f}")

# %% [markdown]
# ## Prevención de SQL Injection
#
# Esto es VULNERABLE:
# ```python
# user_input = "Ana'; DROP TABLE customers; --"
# session.query(Customer).filter(f"name = '{user_input}'").all()
# ```
#
# Con SQLAlchemy ORM, esto es SEGURO:
# ```python
# user_input = "Ana'; DROP TABLE customers; --"
# session.query(Customer).filter(Customer.name == user_input).all()
# # El ORM maneja los parámetros automáticamente
# ```

# %%
# Seguro: SQLAlchemy escapa la entrada automáticamente
dangerous_input = "Ana'; DROP TABLE customers; --"
result = session.query(Customer).filter(Customer.name == dangerous_input).all()
print(f"\nSearch for '{dangerous_input}': {len(result)} results (safe!)")

# %% [markdown]
# ## Manejo de errores de base de datos
#
# IntegrityError: violación de restricciones (unique, foreign key, etc.)
# OperationalError: errores operacionales (tabla no existe, permisos, etc.)


# %%
def add_customer_safe(session: Session, name: str, email: str) -> bool:
    try:
        customer = Customer(name=name, email=email, balance=0.0)
        session.add(customer)
        session.commit()
        print(f"Customer '{name}' added successfully")
        return True

    except IntegrityError as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e):
            print(f"Error: Customer '{name}' or email '{email}' already exists")
        else:
            print(f"Integrity error: {e}")
        return False

    except OperationalError as e:
        session.rollback()
        print(f"Database error: {e}")
        return False

    except Exception as e:
        session.rollback()
        print(f"Unexpected error: {e}")
        return False


# %%
with Session(engine) as session:
    # Intento 1: éxito
    add_customer_safe(session, "Carlos", "carlos@example.com")

    # Intento 2: email duplicado (falla con IntegrityError)
    add_customer_safe(session, "Carlos", "carlos@example.com")

    # Intento 3: nombre duplicado
    add_customer_safe(session, "Ana", "ana2@example.com")

# %% [markdown]
# ## Órdenes con transacción atómica
#
# Crear una orden implica múltiples cambios que deben ser atómicos.


# %%
def create_order_atomic(session: Session, customer_id: int, amount: float):
    try:
        # Verificar cliente existe y tiene fondos
        customer = session.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")

        if customer.balance < amount:
            raise ValueError(f"Insufficient balance: ${customer.balance} < ${amount}")

        # Crear orden
        order = Order(customer_id=customer_id, amount=amount, status="confirmed")
        session.add(order)

        # Restar dinero de cliente (cargar tarjeta)
        customer.balance -= amount

        # Si llegamos aquí, commit hace TODO permanente
        session.commit()
        print(f"Order #{order.id} created: ${amount} charged to {customer.name}")
        return order.id

    except ValueError as e:
        session.rollback()
        print(f"Order creation failed: {e}")
        return None


# %%
with Session(engine) as session:
    # Crear orden para Ana (tiene $400 después de transfer)
    order_id = create_order_atomic(session, customer_id=1, amount=50.0)

    # Intentar orden que excede saldo
    order_id = create_order_atomic(session, customer_id=1, amount=1000.0)

# %%
# Verificar órdenes creadas
with Session(engine) as session:
    all_orders = session.query(Order).all()
    print(f"\nTotal orders: {len(all_orders)}")
    for order in all_orders:
        print(f"  {order}")

# %% [markdown]
# ## Queries útiles para datos operacionales
#
# Cálculos rápidos con SQLAlchemy.

# %%
from sqlalchemy import func

with Session(engine) as session:
    # Total de dinero en órdenes
    total_orders = session.query(func.sum(Order.amount)).scalar() or 0
    print(f"\nTotal order value: ${total_orders:.2f}")

    # Promedio de órdenes
    avg_order = session.query(func.avg(Order.amount)).scalar() or 0
    print(f"Average order: ${avg_order:.2f}")

    # Cantidad de órdenes por cliente
    orders_per_customer = session.query(Customer.name, func.count(Order.id)).outerjoin(Order).group_by(Customer.id).all()
    print("\nOrders per customer:")
    for name, count in orders_per_customer:
        print(f"  {name}: {count} orders")

# %% [markdown]
# ## Resumen
#
# - **Transacciones:** Garantizan que múltiples operaciones se completan juntas
# - **Context managers:** `with Session()` maneja commit/rollback automáticamente
# - **Seguridad:** SQLAlchemy ORM previene SQL injection automáticamente
# - **Errores:** IntegrityError para restricciones, OperationalError para DB
# - **SQLite vs PostgreSQL:** SQLite para single-user, PostgreSQL para multi-user
#
# Próximo: DuckDB para queries analíticas rápidas.
