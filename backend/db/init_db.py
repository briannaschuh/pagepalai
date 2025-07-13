from sqlalchemy import create_engine
from backend.config import DATABASE_URL
from backend.db.base import Base

from backend.db.models.book import Book
from backend.db.models.chunk import Chunk
from backend.db.models.ai_output import AIOutput
from backend.db.models.language_level import LanguageLevel

engine = create_engine(DATABASE_URL)

def create_tables():
    """
    Creates all database tables defined in the SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)