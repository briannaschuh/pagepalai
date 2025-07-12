from backend.db import db

def test_chunks_table_crud():
    # insert a temp book (required for foreign key constraint)
    test_gutenberg_id = 99999998
    db.delete("books", {"gutenberg_id": test_gutenberg_id})  # clean up if exists

    db.insert("books", ["gutenberg_id", "title", "author", "language", "language_level", "source"], [
        test_gutenberg_id, "Temp Book", "Test Author", "es", "A2", "https://example.com"
    ])

    book_id = db.select("books", "id", {"gutenberg_id": test_gutenberg_id})[0]["id"]

    # insert 2 chunks
    db.insert("chunks", ["book_id", "page_number", "text", "embedding"], [
        book_id, 0, "Esto es un chunk de prueba.", [0.1] * 1536  # dummy embedding
    ])
    db.insert("chunks", ["book_id", "page_number", "text", "embedding"], [
        book_id, 1, "Otro chunk para probar.", [0.2] * 1536
    ])

    # SELECT & verify
    chunks = db.select("chunks", "*", {"book_id": book_id})
    assert len(chunks) == 2
    assert chunks[0]["text"] == "Esto es un chunk de prueba."

    # EXISTS
    assert db.exists("chunks", {"book_id": book_id, "page_number": 1}) is True

    # UPDATE one chunk
    db.update("chunks", {"text": "Texto actualizado"}, {"book_id": book_id, "page_number": 1})
    updated = db.select("chunks", "*", {"book_id": book_id, "page_number": 1})
    assert updated[0]["text"] == "Texto actualizado"

    # DELETE chunks and book
    deleted_chunks = db.delete("chunks", {"book_id": book_id})
    deleted_book = db.delete("books", {"id": book_id})
    assert deleted_chunks == 2
    assert deleted_book == 1