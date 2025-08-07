from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB 
from backend.db.base import Base

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    tokens = Column(Integer)
    embedding = Column(Vector(1536))
    chunk_metadata = Column("metadata", JSONB)
    created_at = Column(DateTime, server_default=func.now())

    book = relationship("Book", back_populates="chunks")
    ai_outputs = relationship("AIOutput", back_populates="chunk")

    __table_args__ = (
        UniqueConstraint("book_id", "page_number", name="uq_book_page"),
    )

    def __repr__(self):
        return f"<Chunk(id={self.id}, book_id={self.book_id}, page_number={self.page_number})>"