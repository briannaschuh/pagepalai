from backend.utils.retriever import retrieve_top_chunks
from backend.db.db import select

def test_retrieve_top_chunks_from_gutenberg_id():
    query = "Who is Don Quijote?"
    gutenberg_id = 2000
    
    result = select("books", columns="id", condition={"gutenberg_id": gutenberg_id}) # retrieve internal book_id using Gutenberg ID
    assert result, "Book not found in database"
    
    book_id = result[0]["id"]
    print("Book ID:", book_id)
    chunks = retrieve_top_chunks(query, book_id)

    assert chunks, "No chunks were retrieved"
    assert isinstance(chunks[0], str), "Chunk should be a string"
    print("Retrieved chunks:", chunks)
