from pydantic import BaseModel
from typing import Optional

class ExplainationRequest(BaseModel):
    text: str
    language_level: str
    context_before: Optional[str] = None
    context_after: Optional[str] = None
    book_title: Optional[str] = None
    book_author: Optional[str] = None
    book_language: Optional[str] = None
