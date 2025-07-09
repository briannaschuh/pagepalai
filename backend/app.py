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

import logging

from backend.db.init_db import create_tables
from backend.config import PAGEPAL_API_KEY

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler) # set a limiter

logging.basicConfig(level=logging.INFO) # configure logging
logger = logging.getLogger(__name__)

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
    create_tables()

# function that verifies the API key to hit my backend
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != PAGEPAL_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

# testing purposes
@app.get("/secure", dependencies=[Depends(verify_api_key)])
async def secure_endpoint():
    return {"message": "This is protected!"}

# endpoint to retrieve explanation of a text    
@app.post("/explain", dependencies=[Depends(verify_api_key)])
@limiter.limit("3/minute")
async def explain(request: Request, payload: ExplainationRequest):
    try:
        explanation = await get_explanation(payload.text, payload.language_level)
        return {"explanation": explanation}
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        raise HTTPException(status_code=500, detail="Explanation failed. Please try again later.")