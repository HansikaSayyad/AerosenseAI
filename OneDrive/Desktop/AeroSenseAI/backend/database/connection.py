# backend/database/connection.py

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings

# ─────────────────────────────────────────
# DATABASE ENGINE
# Creates the connection to PostgreSQL
# pool_size = keep 5 connections open always
# max_overflow = allow 10 extra if needed
# ─────────────────────────────────────────
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,   # checks connection is alive before using
    echo=settings.DEBUG   # prints SQL queries in debug mode
)

# ─────────────────────────────────────────
# SESSION FACTORY
# Creates database sessions for each request
# ─────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ─────────────────────────────────────────
# BASE CLASS
# All database models will inherit from this
# ─────────────────────────────────────────
Base = declarative_base()


# ─────────────────────────────────────────
# DEPENDENCY INJECTION FUNCTION
# Used in FastAPI routes to get DB session
# Automatically closes session after request
# ─────────────────────────────────────────
def get_db():
    """
    FastAPI dependency that provides a database session.
    
    Usage in routes:
        @router.get("/")
        def my_route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─────────────────────────────────────────
# TEST CONNECTION FUNCTION
# Used to verify DB is reachable on startup
# ─────────────────────────────────────────
def test_connection():
    """Tests if database connection is working."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Database connected successfully!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False