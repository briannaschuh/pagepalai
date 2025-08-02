from sqlalchemy import Column, String
from backend.db.base import Base

class Language(Base):
    __tablename__ = "language_mapping"

    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Language(code={self.code}, name={self.name})>"