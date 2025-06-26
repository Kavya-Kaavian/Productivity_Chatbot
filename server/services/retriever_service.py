import os
from openai import OpenAI
import pinecone
from difflib import SequenceMatcher

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

    # Semantic search
    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    matches = response.get("matches", [])

    results = []
    for m in matches:
        metadata = m.get("metadata", {})
        text = metadata.get("text", "")
        sim_score = similarity(query, text)

        results.append({
            "id": m["id"],
            "semantic_score": m["score"],
            "metadata_text_match_score": sim_score,
            "metadata": metadata
        })

    # Sort by metadata match score first, then semantic
    results.sort(key=lambda x: (x["metadata_text_match_score"], x["semantic_score"]), reverse=True)

    return {
        "query": query,
        "matches": results
    }