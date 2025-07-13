from fastapi import Header, HTTPException
from backend.config import PAGEPAL_API_KEY

def verify_api_key(x_api_key: str = Header(...)):
    """
    Verifies the API key provided in the request headers.
    """
    if x_api_key != PAGEPAL_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
