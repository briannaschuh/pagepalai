# i needed to rebuild the index since i didn't include metadata the first time it was built
# the metadata is needed to filter the chunks table by book id
from llama_index.core import Settings, Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from sqlalchemy.engine.url import make_url
from backend.db.db import select
from backend.config import DATABASE_URL, OPENAI_EMBEDDINGS

Settings.embed_model = OpenAIEmbedding(model=OPENAI_EMBEDDINGS)

rows = select("chunks", columns="id, text, book_id")

documents = [
    Document(text=row["text"], metadata={"book_id": row["book_id"]})
    for row in rows
]

url = make_url(DATABASE_URL)
vector_store = PGVectorStore.from_params(
    database=url.database,
    host=url.host,
    port=url.port,
    user=url.username,
    password=url.password,
    table_name="chunks",
    embed_dim=1536,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context  
)

print("Vector index rebuilt with metadata and persistent docstore")
