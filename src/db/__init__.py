# db/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Dependency Injection for SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
