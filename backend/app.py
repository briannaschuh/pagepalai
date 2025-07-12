from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pathlib import Path

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse

from backend.schemas.validate import ExplainationRequest
from backend.utils.openai_helpers import get_explanation
from backend.db.init_db import create_tables
from backend.config import PAGEPAL_API_KEY
from backend.utils.logging_config import setup_logger

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler) # set a limiter

logger = setup_logger(__name__)

origins = ["http://localhost:3000", "https://pagepal.ai"] # allows for only my frontend to hit the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    """
    Runs on application startup.

    Creates database tables if they don't already exist.
    """
    create_tables()

# function that verifies the API key to hit my backend
def verify_api_key(x_api_key: str = Header(...)):
    """
    Verifies the API key provided in the request headers.

    Args:
        x_api_key (str): The API key passed in the request header.

    Raises:
        HTTPException: If the API key is invalid.
    """
    if x_api_key != PAGEPAL_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

# testing purposes
@app.get("/secure", dependencies=[Depends(verify_api_key)])
async def secure_endpoint():
    """
    A protected test endpoint to verify API key authentication.

    Returns:
        dict: A success message if authentication passes.
    """
    return {"message": "This is protected!"}

# endpoint to retrieve explanation of a text    
@app.post("/explain", dependencies=[Depends(verify_api_key)])
@limiter.limit("3/minute")
async def explain(request: Request, payload: ExplainationRequest):
    """
    Generates a simplified explanation of a given text for language learners.

    This endpoint calls the OpenAI API to tailor explanations to the user's language level.
    Rate limited to 3 requests per minute.

    Args:
        request (Request): The FastAPI request object (unused, but available for logging).
        payload (ExplainationRequest): Request body containing `text` and `language_level`.

    Returns:
        dict: A JSON response with the explanation text.

    Raises:
        HTTPException: If the OpenAI API call fails.
    """
    try:
        explanation = await get_explanation(payload.text, payload.language_level)
        return {"explanation": explanation}
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        raise HTTPException(status_code=500, detail="Explanation failed. Please try again later.")