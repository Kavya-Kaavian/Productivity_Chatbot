import os
from openai import OpenAI
import pinecone

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")
PINECONE_INDEX_NAME = "productivity"
EMBEDDING_MODEL = "text-embedding-3-large"

client = OpenAI(api_key=OPENAI_API_KEY)
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# === Generate embedding for query ===
def get_query_embedding(query: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    )
    return response.data[0].embedding

# === Metadata filter builder ===
def build_filter(filter_dict: dict):
    return {
        k: {"$eq": v}
        for k, v in filter_dict.items()
        if v is not None and v != ""
    } or None

# === Hybrid Search Function ===
async def search_by_query_service(query: str, top_k: int = 5, filters: dict = None):
    query_vector = get_query_embedding(query)
    metadata_filter = build_filter(filters or {})

    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        filter=metadata_filter
    )

    matches = response.get("matches", [])

    simplified_matches = [
        {
            "id": m["id"],
            "score": m["score"],
            "metadata": m["metadata"]
        }
        for m in matches
    ]

    return {
        "query": query,
        "filters_used": metadata_filter,
        "matches": simplified_matches
    }
