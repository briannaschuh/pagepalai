from backend.db import db

def test_books_table_crud():
    # CLEAN UP
    db.delete("books", {"gutenberg_id": 99999999})

    # INSERT
    db.insert("books", ["gutenberg_id", "title", "author", "language", "language_level", "source"], [
        99999999, "Test Book", "Test Author", "es", "A1", "https://example.com"
    ])

    # SELECT
    results = db.select("books", "*", {"gutenberg_id": 99999999})
    assert len(results) == 1
    assert results[0]["author"] == "Test Author"

    # EXISTS
    assert db.exists("books", {"gutenberg_id": 99999999}) is True

    # UPDATE
    db.update("books", {"author": "Updated Author"}, {"gutenberg_id": 99999999})
    updated = db.select("books", "*", {"gutenberg_id": 99999999})
    assert updated[0]["author"] == "Updated Author"

    # DELETE
    deleted = db.delete("books", {"gutenberg_id": 99999999})
    assert deleted == 1
