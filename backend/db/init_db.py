from sqlalchemy import create_engine
import os

from backend.db.base import Base
from backend.config import DATABASE_URL
from backend.db.models.models import Book, Chunk, AIOutput

# create a SQLAlchemy engine using the database URL from config
engine = create_engine(DATABASE_URL)

# create tables based on models.py
def create_tables():
    """
    Creates all database tables defined in the SQLAlchemy models.

    Uses metadata from Base to generate tables like Book, Chunk, and AIOutput
    if they don't already exist in the database.
    """
    Base.metadata.create_all(bind=engine)