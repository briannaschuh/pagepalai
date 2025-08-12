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
from backend.config import PAGEPAL_API_KEY
from backend.utils.logging_config import setup_logger
from backend.utils.auth_utils import verify_api_key

from backend.routers import books, chunks

app = FastAPI(
    title="LLM Reading Tutor API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Books",
            "description": "Operations related to book metadata and content chunks."
        },
        {
            "name": "Chunks",
            "description": "Operations related to managing chunks."
        },
        {
            "name": "AI",
            "description": "Endpoints that use AI, like explanations and summaries."
        }
    ]
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler) # set a limiter

logger = setup_logger(__name__)

origins = ["http://localhost:3000", "https://pagepal.ai", "http://localhost:5173"] # allows for only my frontend to hit the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(chunks.router)

# testing purposes
@app.get("/secure", 
         summary="API key verification",
         description="Endpoint used to ensure that API key authentication is working as expected",
         tags=["Security"],
         dependencies=[Depends(verify_api_key)])
async def secure_endpoint():
    """
    A protected test endpoint to verify API key authentication.

    Returns:
        dict: A success message if authentication passes.
    """
    return {"message": "This is protected!"}

# endpoint to retrieve explanation of a text    
@app.post("/explain", 
          summary="Explanation of text",
          description="Returns an explanation of the text provided",
          tags=["AI"],
          dependencies=[Depends(verify_api_key)])
@limiter.limit("3/minute")
async def explain(request: Request, payload: ExplainationRequest):
    try:
        explanation = await get_explanation(
            text=payload.text,
            level=payload.language_level,
            context_before=payload.context_before,
            context_after=payload.context_after,
            book_title=payload.book_title,
            book_author=payload.book_author,
            book_language=payload.book_language,
        )
        return {"explanation": explanation}
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        raise HTTPException(status_code=500, detail="Explanation failed. Please try again later.")