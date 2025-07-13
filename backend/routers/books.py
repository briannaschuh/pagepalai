from fastapi import APIRouter, Depends
from backend.utils.books_utils import get_all_books
from backend.utils.auth_utils import verify_api_key

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException
from backend.utils.auth_utils import verify_api_key
from backend.utils.books_utils import (
    get_all_books, 
    get_languages, 
    get_levels_for_language, 
    get_books_by_language_and_level
)

router = APIRouter()

@router.get("/books", 
            summary="List books",
            description="Returns a list of books with metadata like title, author, language, and language level.",
            tags=["Books"],
            dependencies=[Depends(verify_api_key)]
            )
def list_books():
    return get_all_books()

@router.get("/languages", 
            summary="List available languages",
            description="Returns a list of languages supported by the platform",
            tags=["Books"],
            dependencies=[Depends(verify_api_key)]
            )
def list_languages():
    return get_languages()

@router.get("/levels/{language}", 
            summary="List CEFR levels for a given language",
            description="Returns a list of CERF levels for a given language",
            tags=["Books"],
            dependencies=[Depends(verify_api_key)]
            )
def list_levels(language: str):
    levels = get_levels_for_language(language)
    if not levels:
        raise HTTPException(status_code=404, detail="Language not found")
    return levels

@router.get("/books/{language}/{level}",
            summary="Get books by language and level", 
            description="Returns a list of books given the language and level",
            tags=["Books"],
            dependencies=[Depends(verify_api_key)]
            )
def books_by_lang_level(language: str, level: str):
    books = get_books_by_language_and_level(language, level)
    if not books:
        raise HTTPException(status_code=404, detail="No books found for this language/level")
    return books