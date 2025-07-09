from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from pgvector.sqlalchemy import Vector
from datetime import datetime

from backend.db.base import Base

# -------------------------
# Book Table
# -------------------------
class Book(Base):
    __tablename__ = "books"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String)
    language = Column(String)
    source = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    chunks = relationship("Chunk", back_populates="book")


# -------------------------
# Chunk Table
# -------------------------
class Chunk(Base):
    __tablename__ = "chunks"
    
    # columns
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    tokens = Column(Integer)
    embedding = Column(Vector(1536))
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    book = relationship("Book", back_populates="chunks")
    ai_outputs = relationship("AIOutput", back_populates="chunk")


# -------------------------
# AI Output Table
# -------------------------
class AIOutput(Base):
    __tablename__ = "aioutput"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("chunks.id"), nullable=False)
    type = Column(String, nullable=False)  
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    chunk = relationship("Chunk", back_populates="ai_outputs")