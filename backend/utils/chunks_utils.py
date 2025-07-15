from backend.db import db

def get_chunk_by_page(gutenberg_id: int, page: int, limit: int = 1):
    """
    Retrieves a specific chunk for a book by its Gutenberg ID and page number.

    Args:
        gutenberg_id (int): The Project Gutenberg ID of the book.
        page (int): Page number to fetch (1-indexed).
        limit (int): Number of chunks per page (default 1).

    Returns:
        dict: Contains pagination info and the chunk.
    """
    offset = (page - 1) * limit

    # Step 1: Look up internal book_id using gutenberg_id
    book_lookup = db.raw(
        "SELECT id FROM books WHERE gutenberg_id = :gutenberg_id",
        {"gutenberg_id": gutenberg_id}
    )

    if not book_lookup:
        return None  # Book not found

    book_id = book_lookup[0]["id"]

    # Step 2: Count total chunks for that book_id
    total_chunks_result = db.raw(
        "SELECT COUNT(*) as count FROM chunks WHERE book_id = :book_id",
        {"book_id": book_id}
    )
    total_chunks = total_chunks_result[0]['count']
    total_pages = (total_chunks + limit - 1) // limit

    if page > total_pages or page < 1:
        return None

    # Step 3: Fetch the chunk for that page
    chunk_result = db.raw("""
        SELECT id as chunk_id, text
        FROM chunks
        WHERE book_id = :book_id
        ORDER BY id
        LIMIT :limit OFFSET :offset
    """, {
        "book_id": book_id,
        "limit": limit,
        "offset": offset
    })

    return {
        "gutenberg_id": gutenberg_id,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "total_chunks": total_chunks,
        "chunk": chunk_result[0] if chunk_result else None
    }
