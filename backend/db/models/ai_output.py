from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.db.base import Base

class AIOutput(Base):
    __tablename__ = "aioutput"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("chunks.id"), nullable=False)
    type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    chunk = relationship("Chunk", back_populates="ai_outputs")

    def __repr__(self):
        return f"<AIOutput(id={self.id}, chunk_id={self.chunk_id}, type={self.type})>"
