from openai import OpenAI
import os

def generate_embedding(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=[text],
        model=os.getenv("EMBEDDING_MODEL")
        )
    return response.data[0].embedding