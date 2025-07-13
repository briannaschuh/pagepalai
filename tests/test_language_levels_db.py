from backend.db import db

def test_language_levels_table_crud():
    # CLEAN UP (in case it already exists)
    db.delete("language_levels", {"language": "zz", "level": "Z9"})

    # INSERT
    inserted = db.insert("language_levels", ["language", "level"], ["zz", "Z9"])
    assert inserted == 1

    # SELECT
    results = db.select("language_levels", "*", {"language": "zz", "level": "Z9"})
    assert len(results) == 1
    assert results[0]["language"] == "zz"
    assert results[0]["level"] == "Z9"

    # EXISTS
    assert db.exists("language_levels", {"language": "zz", "level": "Z9"}) is True

    # DELETE
    deleted = db.delete("language_levels", {"language": "zz", "level": "Z9"})
    assert deleted == 1
