import openai
import os
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_embedding(text: str):
    response = openai_client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=[text]
    )
    return response.data[0].embedding