from openai import OpenAI
import os
from dotenv import load_dotenv

openai_client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
def generate_embedding(text: str):
    response = openai_client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=[text]
    )
    return response.data[0].embedding