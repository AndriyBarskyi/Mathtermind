# database/init_db.py
from .models import Base
from . import engine

def init_db():
    """Initialize the database schema."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
