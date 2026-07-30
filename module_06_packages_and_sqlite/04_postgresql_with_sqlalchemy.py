# %% [markdown]
# # 04. PostgreSQL con SQLAlchemy
#
# ## Objetivos
#
# - Conectar a PostgreSQL (servidor real, no archivo local)
# - Usar SQLAlchemy con bases de datos empresariales
# - Entender diferencias entre SQLite y PostgreSQL
# - Manejar connection pooling

# %% [markdown]
# ## SQLite vs PostgreSQL
#
# | Aspecto | SQLite | PostgreSQL |
# |---------|--------|-----------|
# | Instalación | 0 - Integrado | Requiere servidor |
# | Concurrencia | 1 escritor | Múltiples escritores |
# | Escala | MB-GB | GB-TB+ |
# | Networking | Archivo local | Cliente-servidor |
# | Transacciones | ACID | ACID avanzado |
# | Uso | Desarrollo, Desktop | Producción, Web |
#
# **Regla:** SQLite para desarrollo local, PostgreSQL para producción.

# %% [markdown]
# ## Configuración PostgreSQL
#
# ```bash
# # En tu Mac (si usas Homebrew)
# brew install postgresql
# brew services start postgresql
#
# # Crear usuario y base de datos
# createdb inventory
# createuser -P inventory_user  # Te pide contraseña
# ```

# %%
from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, declarative_base, relationship
from sqlalchemy.pool import QueuePool

# %% [markdown]
# ## Configuración de conexión PostgreSQL
#
# Format: `postgresql://usuario:contraseña@host:puerto/base_datos`

# %%
# Configuración - CAMBIAR estos valores según tu instalación
POSTGRES_USER = "inventory_user"
POSTGRES_PASSWORD = "your_password"  # TODO: Cambiar a tu contraseña
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "inventory"

# Construir URL de conexión
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print(f"Connecting to: postgresql://{POSTGRES_USER}:***@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

Base = declarative_base()


# %% [markdown]
# ## Modelos (idénticos a SQLite)

# %%
class Customer(Base):
    __tablename__ = "customers"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False, unique=True)
    email: str = Column(String(100), nullable=False, unique=True)
    balance: float = Column(Float, default=0.0)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

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


# %% [markdown]
# ## Connection Pool
#
# PostgreSQL es cliente-servidor, así que reutilizamos conexiones con un pool.
# QueuePool maneja varias conexiones para múltiples threads/procesos.

# %%
engine = create_engine(
    DATABASE_URL,
    echo=False,
    poolclass=QueuePool,
    pool_size=5,  # Conexiones en el pool
    max_overflow=10,  # Conexiones adicionales cuando se necesita
    pool_recycle=3600,  # Reciclar conexiones cada 1 hora
)

# Crear tablas
try:
    Base.metadata.create_all(engine)
    print("✓ Tables created successfully")
except OperationalError as e:
    print(f"✗ Database connection failed: {e}")
    print(f"  Make sure PostgreSQL is running and credentials are correct")
    exit(1)


# %% [markdown]
# ## Transacciones (igual que SQLite)

# %%
def transfer_money(session: Session, from_id: int, to_id: int, amount: float):
    try:
        # Paso 1: Verificar y restar
        from_customer = session.query(Customer).filter(Customer.id == from_id).first()
        if not from_customer:
            raise ValueError(f"Customer {from_id} not found")

        if from_customer.balance < amount:
            raise ValueError(f"Insufficient funds. Balance: ${from_customer.balance}")

        from_customer.balance -= amount

        # Paso 2: Sumar a destino
        to_customer = session.query(Customer).filter(Customer.id == to_id).first()
        if not to_customer:
            raise ValueError(f"Customer {to_id} not found")

        to_customer.balance += amount

        # Ambas operaciones se cometen juntas
        session.commit()
        print(f"✓ Transfer: ${amount} from {from_customer.name} to {to_customer.name}")

    except ValueError as e:
        session.rollback()
        print(f"✗ Transfer failed: {e}")
        raise


# %% [markdown]
# ## Crear datos de prueba

# %%
# Limpiar datos previos
with Session(engine) as session:
    session.query(Order).delete()
    session.query(Customer).delete()
    session.commit()
    print("✓ Cleaned previous data")

# Crear nuevos clientes
with Session(engine) as session:
    customers = [
        Customer(name="Alice", email="alice@example.com", balance=1000.0),
        Customer(name="Bob", email="bob@example.com", balance=500.0),
        Customer(name="Charlie", email="charlie@example.com", balance=750.0),
    ]
    session.add_all(customers)
    session.commit()
    print(f"✓ Created {len(customers)} customers")


# %% [markdown]
# ## Transacciones en PostgreSQL

# %%
with Session(engine) as session:
    # Transferencia exitosa
    transfer_money(session, from_id=1, to_id=2, amount=100.0)

    # Transferencia que falla (insuficientes fondos)
    try:
        transfer_money(session, from_id=2, to_id=1, amount=10000.0)
    except ValueError:
        pass


# %% [markdown]
# ## Manejo de errores PostgreSQL

# %%
def add_customer_safe(session: Session, name: str, email: str) -> bool:
    try:
        customer = Customer(name=name, email=email, balance=0.0)
        session.add(customer)
        session.commit()
        print(f"✓ Customer '{name}' added")
        return True

    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e).lower():
            print(f"✗ Customer '{name}' or email '{email}' already exists")
        else:
            print(f"✗ Integrity error: {e}")
        return False

    except OperationalError as e:
        session.rollback()
        print(f"✗ Database error: {e}")
        return False


# %%
with Session(engine) as session:
    # Éxito
    add_customer_safe(session, "Diana", "diana@example.com")

    # Falla: duplicado
    add_customer_safe(session, "Alice", "alice2@example.com")


# %% [markdown]
# ## Queries avanzadas (específicas de PostgreSQL)

# %%
from sqlalchemy import func

with Session(engine) as session:
    # Contar clientes
    total_customers = session.query(func.count(Customer.id)).scalar()
    print(f"\nTotal customers: {total_customers}")

    # Balance promedio
    avg_balance = session.query(func.avg(Customer.balance)).scalar()
    print(f"Average balance: ${avg_balance:.2f}")

    # Total en órdenes
    total_orders_value = session.query(func.sum(Order.amount)).scalar() or 0
    print(f"Total orders value: ${total_orders_value:.2f}")

    # Clientes con sus órdenes (JOIN)
    customer_orders = (
        session.query(
            Customer.name,
            func.count(Order.id).label("order_count"),
            func.sum(Order.amount).label("total_spent")
        )
        .outerjoin(Order)
        .group_by(Customer.id)
        .all()
    )

    print("\nCustomers and orders:")
    for name, count, total in customer_orders:
        print(f"  {name}: {count} orders, ${total or 0:.2f}")


# %% [markdown]
# ## Ventajas de PostgreSQL
#
# - **Concurrencia:** Múltiples usuarios escribiendo simultáneamente
# - **Escalabilidad:** Maneja millones de registros eficientemente
# - **Características avanzadas:** JSON, arrays, full-text search
# - **Confiabilidad:** ACID completo, replicación, backups
# - **Seguridad:** Autenticación, permisos granulares

# %% [markdown]
# ## Resumen: Cuándo usar cada una
#
# **SQLite:**
# - Desarrollo local
# - Desktop apps
# - Single-user applications
# - Mobile apps (con SQLite embebido)
#
# **PostgreSQL:**
# - Producción web
# - Múltiples usuarios concurrentes
# - Datos críticos
# - Escalabilidad requerida
# - Team projects

print("\n✓ PostgreSQL connection demo complete!")
