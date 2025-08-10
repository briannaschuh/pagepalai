
import argparse
import requests
import re
import time
from tenacity import retry, wait_random_exponential, stop_after_attempt
from openai import OpenAI
from tqdm import tqdm
from sqlalchemy.exc import IntegrityError
import logging

from backend.db import db
from backend import config
from backend.utils.logging_config import setup_logger

logging.getLogger("httpx").setLevel(logging.WARNING) # so that the command line doesn't show these two logs
logging.getLogger("httpcore").setLevel(logging.WARNING)

CHUNK_SIZE = 100 
RETRY_ATTEMPTS = 3 
client = OpenAI(api_key=config.OPENAI_API_KEY)
embeddings_model = config.OPENAI_EMBEDDINGS
timeout = 15
retry_settings = dict(wait=wait_random_exponential(min=1, max=4), stop=stop_after_attempt(RETRY_ATTEMPTS))

@retry(**retry_settings)
def fetch_metadata_from_gutendex(book_id: int) -> dict:
    """
    Fetches metadata for a given book ID from Gutendex

    Args:
        book_id (int): ID of the book

    Raises:
        Exception: if it fails to retrieve the metadata or it fails to find a plain text file for the book

    Returns:
        dict: Contains metadata including title, author, language, text URL, and encoding.
    """
    response = requests.get(
        f"https://gutendex.com/books/{book_id}",
        headers={"User-Agent": "Mozilla/5.0 (compatible; MyBookApp/0.1)"},
    timeout=timeout
    )
    if response.status_code != 200:
        raise Exception(f"Failed to fetch metadata for book ID {book_id}")
    data = response.json()

    title = data.get("title", "Unknown Title")
    language = data.get("languages", ["unknown"])[0]
    authors = data.get("authors", [])
    author = authors[0].get("name") if authors else "unknown"

    text_url = None
    encoding = "utf-8"  # fallback

    # looking for a good .txt format to download
    for preferred_encoding in ["utf-8", "us-ascii", "iso-8859-1"]:
        for key, url in data.get("formats", {}).items():
            if key.startswith("text/plain") and url.endswith(".txt") and preferred_encoding in key:
                text_url = url
                encoding = preferred_encoding
                break
        if text_url:
            break

    # if a good text format wasn't found, we just just default format is available in that URL
    if not text_url:
        fallback_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
        head = requests.head(fallback_url)
        if head.status_code == 200:
            text_url = fallback_url
            encoding = "utf-8"
        else:
            raise Exception(f"No plain text format found for thhe book ID {book_id}")

    return {
        "title": title,
        "author": author,
        "text_url": text_url,
        "source_url": f"https://www.gutenberg.org/ebooks/{book_id}",
        "language": language,
        "encoding": encoding
    }

@retry(**retry_settings)
def download_text(url: str, encoding: str = "utf-8") -> str:
    """
    Downloads the raw text of the book from the given URL.

    Args:
        url (str): URL pointing to the plain text file.
        encoding (str, optional): Text encoding format (default is "utf-8").

    Raises:
        Exception: If the text cannot be downloaded (non-200 status code).

    Returns:
        str: Raw book text as a single string.
    """
    response = requests.get(
        url, 
        headers={"User-Agent": "Mozilla/5.0 (compatible; MyBookApp/0.1)"}, 
        timeout=timeout
        )
    if response.status_code != 200:
        raise Exception("Failed to download book text.")
    response.encoding = encoding
    return response.text

def clean_text(raw_text: str) -> str:
    """
    Removes boilerplate and license content from the raw book text using START/END markers.

    Args:
        raw_text (str): Raw book text including headers and footers.

    Returns:
        str: Cleaned book content with only the actual story/text.
    """
    start = re.search(r"\*\*\*\s*START OF.*?\*\*\*", raw_text, re.IGNORECASE) # many text files tend to say when the book text actually starts, noted by "START OF..."
    end = re.search(r"\*\*\*\s*END OF.*?\*\*\*", raw_text, re.IGNORECASE) # many text files tend to say when the book text ends, noted by "END OF..."

    if start and end:
        return raw_text[start.end():end.start()].strip()
    elif start:
        return raw_text[start.end():].strip()
    elif end:
        return raw_text[:end.start()].strip()
    else:
        print("No START/END markers found in the text.")
        return raw_text.strip()

def split_into_chunks(cleaned: str, max_words=CHUNK_SIZE):
    """
    Splits the cleaned book text into chunks of up to `max_words` words each.

    Args:
        cleaned (str): Cleaned book text (without headers/footers).
        max_words (int, optional): Maximum number of words per chunk (default is CHUNK_SIZE).

    Returns:
        list[str]: List of text chunks.
    """
    words = cleaned.split()
    return [' '.join(words[i:i + max_words]).strip() for i in range(0, len(words), max_words)]

@retry(**retry_settings)
def get_embedding(text: str) -> list[float]:
    """
    Computes the embedding vector for a given chunk of text using the OpenAI API.

    Args:
        text (str): A single chunk of book text.

    Returns:
        list[float]: Embedding vector representing the chunk.
    """
    response = client.embeddings.create(
        model=embeddings_model,
        input=text
    )
    return response.data[0].embedding

def insert_book_and_chunks(book_info: dict, chunks: list[str], dry_run: bool = False):
    """
    Insert book and chunks into their respective tables

    Args:
        book_info (dict): Book metadata
        chunks (list[str]): List of chunks
        dry_run (bool, optional): If dry_run, the insertion won't actually happen
    """
    existing = db.select("books", "*", {"gutenberg_id": book_info["gutenberg_id"]})
    if existing:
        print(f"Book with gutenberg_id={book_info['gutenberg_id']} already exists. Skipping insert.")
        logger.warning(f"Book {book_info['gutenberg_id']} already exists")
        return

    if not dry_run:
        db.insert("books",
            ["gutenberg_id", "title", "author", "language", "language_level", "source"],
            [book_info["gutenberg_id"], book_info["title"], book_info["author"], book_info["language"], book_info["level"], book_info["source_url"]]
        )

    record = db.select("books", "*", {"gutenberg_id": book_info["gutenberg_id"]})
    book_id = record[0]["id"]
    failed_chunks = []

    for i, chunk_text in enumerate(tqdm(chunks, desc="Embedding chunks")):
        try:
            if dry_run:
                logger.info(f"[Dry Run] Would embed and insert chunk {i}")
                continue

            embedding = get_embedding(chunk_text)
            try:
                metadata = {"book_id": book_id}
                db.insert("chunks",
                        ["book_id", "page_number", "text", "embedding", "metadata"],
                        [book_id, i, chunk_text, embedding, metadata])
            except IntegrityError:
                logger.warning(f"Duplicate chunk skipped: book_id={book_id}, page_number={i}")
                continue

            if (i + 1) % 100 == 0 or (i + 1) == len(chunks):
                print(f"Progress: Inserted {i + 1}/{len(chunks)} chunks")

        except Exception as e:
            logger.error(f"Embedding failed for chunk {i}: {e}")
            failed_chunks.append((i, chunk_text))

        time.sleep(0.5)

    for attempt in range(1, 4):
        if not failed_chunks:
            break
        logger.info(f"Retrying {len(failed_chunks)} failed chunks: Attempt {attempt}")
        new_failed = []
        for i, chunk_text in failed_chunks:
            try:
                embedding = get_embedding(chunk_text)
                metadata = {"book_id": book_id}
                db.insert("chunks",
                        ["book_id", "page_number", "text", "embedding", "metadata"],
                        [book_id, i, chunk_text, embedding, metadata])
            except Exception as e:
                logger.error(f"Retry {attempt} failed for chunk {i}: {e}")
                new_failed.append((i, chunk_text))
            time.sleep(0.5)
        failed_chunks = new_failed

    if failed_chunks:
        logger.warning(f"Final failed chunks: {[i for i, _ in failed_chunks]}")
    print(f"Inserted {len(chunks) - len(failed_chunks)} of {len(chunks)} chunks")
    logger.info(f"Book {book_info['gutenberg_id']} inserted with {len(chunks) - len(failed_chunks)} chunks (failed: {len(failed_chunks)})")


def main():
    parser = argparse.ArgumentParser(description="Add a Project Gutenberg book via Gutendex")
    parser.add_argument("--id", type=int, required=True, help="Gutenberg book ID")
    parser.add_argument("--level", type=str, required=True, help="Language level (e.g. A1, A2)")
    parser.add_argument("--dry-run", action="store_true", help="Run script without inserting into database")
    args = parser.parse_args()
    
    global logger
    logger = setup_logger(
        __name__,
        log_file=f"logs/log_book_{args.id}.log"
    )


    print(f"Fetching metadata for book ID {args.id}...")
    metadata = fetch_metadata_from_gutendex(args.id)

    print(f"{metadata['title']} by {metadata['author']}")
    print(f"Language: {metadata['language']}")
    print(f"Downloading from: {metadata['text_url']}")
    raw = download_text(metadata["text_url"], metadata["encoding"])

    cleaned = clean_text(raw)

    print("Showing first 300 characters:")
    print("─" * 60)
    print(cleaned[:300])
    print("─" * 60)

    confirm = input("Do you want to insert this book into the database? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    chunks = split_into_chunks(cleaned)
    book_info = {
        "gutenberg_id": args.id,
        "title": metadata["title"],
        "author": metadata["author"],
        "language": metadata["language"],
        "level": args.level,
        "source_url": metadata["source_url"]
    }

    insert_book_and_chunks(book_info, chunks, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
    print("The book and its chunks have been inserted into their respective tables")