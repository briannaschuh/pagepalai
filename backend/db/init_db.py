from sqlalchemy import create_engine
import os

from backend.db.base import Base
from backend.config import DATABASE_URL
from backend.db.models.models import Book, Chunk, AIOutput

# create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# create tables based on models.py
def create_tables():
    Base.metadata.create_all(bind=engine)