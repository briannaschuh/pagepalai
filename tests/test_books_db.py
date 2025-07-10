from backend.db import db

def test_insert_select_update_delete():
    # CLEAN UP
    db.delete("books", {"title": "Test Book"})

    # INSERT
    db.insert("books", ["title", "author", "language", "language_level", "source"], [
        "Test Book", "Test Author", "es", "A1", "https://example.com"
    ])

    # SELECT
    results = db.select("books", "*", {"title": "Test Book"})
    assert len(results) == 1
    assert results[0]["author"] == "Test Author"

    # EXISTS
    assert db.exists("books", {"title": "Test Book"}) is True

    # UPDATE
    db.update("books", {"author": "Updated Author"}, {"title": "Test Book"})
    updated = db.select("books", "*", {"title": "Test Book"})
    assert updated[0]["author"] == "Updated Author"

    # DELETE
    deleted = db.delete("books", {"title": "Test Book"})
    assert deleted == 1