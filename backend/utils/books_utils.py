from backend.db import db

def get_all_books():
    """
    Retrieves all books from the books table.

    Returns:
        list[dict]: List of books with id, title, author, language, and language level.
    """
    return db.select("books", columns="id, title, author, language, language_level")

def get_language_mappings():
    """
    Returns list of all available language codes and labels.

    Returns:
        list[dict]: List of {code, name} pairs.
    """
    return db.select("language_mapping", columns="code, name")

def get_languages():
    """
    Retrieves distinct languages from the language_levels table.

    Returns:
        list[dict]: List of available languages.
    """
    return db.select("language_levels", columns="DISTINCT language")

def get_levels_for_language(language: str):
    """
    Retrieves CEFR levels for a given language.

    Args:
        language (str): The language to filter levels by.

    Returns:
        list[dict]: List of levels for the language.
    """
    return db.select("language_levels", columns="level", condition={"language": language})

def get_books_by_language_and_level(language: str, level: str):
    """
    Retrieves books matching the given language and CEFR level.

    Args:
        language (str): Book language.
        level (str): CEFR level (e.g., A1, B2).

    Returns:
        list[dict]: List of matching books.
    """
    return db.select("books", columns="id, title, author, language, language_level", condition={
        "language": language,
        "language_level": level
    })
