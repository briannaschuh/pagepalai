from llama_index.core import Settings, VectorStoreIndex, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.vector_stores.types import MetadataFilters, MetadataFilter

from sqlalchemy.engine.url import make_url

from backend.config import DATABASE_URL, OPENAI_EMBEDDINGS, OPENAI_MODEL

from tenacity import retry, stop_after_attempt, wait_random_exponential

def get_pgvector_store(book_id: int) -> PGVectorStore:
    """
    Initializes a PGVectorStore for a specific book using LlamaIndex's pgvector integration.

    Args:
        book_id (int): The ID of the book to scope the vector collection.

    Returns:
        PGVectorStore: A vector store object connected to the given book's embedding collection.
    """
    url = make_url(DATABASE_URL)
    return PGVectorStore.from_params(
        database=url.database,
        host=url.host,
        port=url.port,
        user=url.username,
        password=url.password,
        table_name="chunks",  
        embed_dim=1536
    )

def get_vector_index(book_id: int) -> VectorStoreIndex:
    """
    Builds a VectorStoreIndex for the given book using its associated PGVectorStore.

    Args:
        book_id (int): The ID of the book for which the index is constructed.

    Returns:
        VectorStoreIndex: An index used to retrieve semantically similar chunks from the vector DB.
    """
    vector_store = get_pgvector_store(book_id)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    Settings.embed_model = OpenAIEmbedding(model=OPENAI_EMBEDDINGS)
    Settings.llm = OpenAI(model=OPENAI_MODEL)

    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
    )

@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(min=1, max=3))
def retrieve_top_chunks(query: str, book_id: int, top_k: int = 5) -> list[str]:
    """
    Retrieves the top-k semantically similar chunks from the vector store for a given query.

    Filters results to only include chunks belonging to the specified book_id.
    """
    index = get_vector_index(book_id)
    
    filters = MetadataFilters(filters=[MetadataFilter(key="book_id", value=book_id)])
    retriever = index.as_retriever(similarity_top_k=top_k, filters=filters)

    results = retriever.retrieve(query)
    return [node.get_content() for node in results]