from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from backend.db.base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    gutenberg_id = Column(Integer, unique=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String)
    language = Column(String, nullable=False)
    language_level = Column(String, nullable=False)
    source = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    chunks = relationship("Chunk", back_populates="book")

    __table_args__ = (
        ForeignKeyConstraint(
            ["language", "language_level"],
            ["language_levels.language", "language_levels.level"],
            name="fk_books_language_level"
        ),
    )

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"
