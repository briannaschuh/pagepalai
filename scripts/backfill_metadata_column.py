# i created this script because i forgot to add metadata to the chunks 
# i modified my add_book.py script so that will add the metadata - so i don't need to run this script again
from backend.db.db import select, update
from tqdm import tqdm
from psycopg2.extras import Json

def backfill_metadata_column():
    rows = select("chunks", columns="id, book_id", condition={})  # get all rows

    print(f"Updating metadata for {len(rows)} chunks...")

    for row in tqdm(rows, desc="Backfilling metadata"):
        chunk_id = row["id"]
        book_id = row["book_id"]

        metadata = {"book_id": book_id}
        update("chunks", data={"metadata": Json(metadata)}, update_condition={"id": chunk_id})

    print("Metadata column successfully backfilled.")

if __name__ == "__main__":
    backfill_metadata_column()
