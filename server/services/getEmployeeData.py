import os
from openai import OpenAI
from pinecone import Pinecone
from dotenv import load_dotenv

# Load from .env
load_dotenv()

# Validate required environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Check for missing API keys early
if not openai_api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment or .env")

if not pinecone_api_key:
    raise ValueError("Missing PINECONE_API_KEY in environment or .env")

# Initialize clients
openai_client = OpenAI(api_key=openai_api_key)
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

def get_query_vector(text: str):
    """Generate vector embedding using OpenAI SDK v1."""
    response = openai_client.embeddings.create(
        input=[text],
        model=embedding_model
    )
    return response.data[0].embedding

def search_vector_db(query_text: str, top_k: int = 5, filters: dict = None):
    """Search Pinecone vector database using OpenAI embeddings."""
    vector = get_query_vector(query_text)
    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
        filter=filters or {}
    )
    return results["matches"]
