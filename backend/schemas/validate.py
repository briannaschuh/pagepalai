from pydantic import BaseModel
    
class ExplainationRequest(BaseModel):
    text: str
    language_level: str