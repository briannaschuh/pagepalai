from sqlalchemy import Column, String
from backend.db.base import Base

class LanguageLevel(Base):
    __tablename__ = "language_levels"

    language = Column(String, primary_key=True)
    level = Column(String, primary_key=True)

    def __repr__(self):
        return f"<LanguageLevel(language={self.language}, level={self.level})>"
