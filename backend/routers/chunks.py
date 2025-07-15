from fastapi import APIRouter, Depends, HTTPException, Query
from backend.utils.auth_utils import verify_api_key
from backend.utils.chunks_utils import get_chunk_by_page

router = APIRouter()

@router.get("/book/{gutenberg_id}/chunks",
            summary="Get a specific chunk of a book",
            description="Returns a chunk of text for a specific book and page number",
            tags=["Chunks"],
            dependencies=[Depends(verify_api_key)]
            )
def get_book_chunk(gutenberg_id: int, page: int = Query(1, ge=1), limit: int = Query(1, ge=1)):
    result = get_chunk_by_page(gutenberg_id, page, limit)
    if not result:
        raise HTTPException(status_code=404, detail="Page out of range or book not found")
    return result
