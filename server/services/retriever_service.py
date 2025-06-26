import os
from openai import OpenAI
import pinecone
from difflib import SequenceMatcher
from services.metadata_extraction import extract_metadata_from_query

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "productivity"
EMBEDDING_MODEL = "text-embedding-3-large"

client = OpenAI(api_key=OPENAI_API_KEY)
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

def get_query_embedding(query: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    )
    return response.data[0].embedding

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

async def search_by_query_service(query: str, top_k: int = 5):
    query_vector = get_query_embedding(query)

    # Dynamic metadata extraction
    inferred_metadata = extract_metadata_from_query(query)

    # Convert to Pinecone filter format
    pinecone_filter = {
        k: {"$eq": v}
        for k, v in inferred_metadata.items()
        if v not in [None, ""]
    } or None

    # Search Pinecone
    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        filter=pinecone_filter
    )

    return {
        "query": query,
        "inferred_filter": inferred_metadata,
        "matches": [
            {
                "id": m["id"],
                "score": m["score"],
                "metadata": m["metadata"]
            } for m in response.get("matches", [])
        ]
    }