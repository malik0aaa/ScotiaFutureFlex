"""
database.py — SQLAlchemy engine, session factory, and Base class.
Every other file imports from here.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite file will be created in the same directory as main.py.
# The three slashes mean a relative path: ./scotia.db
DATABASE_URL = "sqlite:///./scotia.db"

# The engine is the low-level connection to the database.
# check_same_thread=False is required for SQLite when used with FastAPI
# because FastAPI can handle a request across multiple threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal is a factory: calling SessionLocal() gives you a new
# database session. autocommit=False means we control when to commit.
# autoflush=False means SQLAlchemy won't auto-sync before every query.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base is the parent class for all SQLAlchemy models (User, Portfolio, etc.).
# When models inherit from Base, SQLAlchemy knows how to map them to tables.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency — injected into route handlers via Depends(get_db).
    Opens a session at the start of a request and guarantees it is closed
    when the request finishes, even if an exception is raised.
    """
    db = SessionLocal()
    try:
        yield db          # hand the session to the route handler
    finally:
        db.close()        # always close, no matter what
