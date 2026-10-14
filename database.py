"""
Database Engine & Session Configuration
Supports PostgreSQL (in Docker) with automatic local SQLite fallback for independent testing.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# Database Connection URLs
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/fastapi_db")
LOCAL_DATABASE_URL = os.getenv("LOCAL_DATABASE_URL", f"sqlite:///{BASE_DIR}/app.db")

# Connection setup with automatic fallback to SQLite if PostgreSQL is unreachable (e.g. outside Docker)
def get_working_engine():
    """Attempts to connect to DATABASE_URL; falls back to SQLite if host is unreachable."""
    target_url = DATABASE_URL
    if target_url.startswith("sqlite"):
        return create_engine(target_url, connect_args={"check_same_thread": False})
    
    try:
        # Quick connection probe for PostgreSQL
        probe_engine = create_engine(target_url, pool_pre_ping=True, connect_args={"connect_timeout": 2})
        with probe_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return probe_engine
    except Exception as e:
        print(f"[Database] Notice: PostgreSQL at {target_url} not reachable ({e}). Using local fallback: {LOCAL_DATABASE_URL}")
        return create_engine(LOCAL_DATABASE_URL, connect_args={"check_same_thread": False})

engine = get_working_engine()

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base for ORM Entities
Base = declarative_base()


def get_db():
    """FastAPI Dependency / Context Manager providing a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
