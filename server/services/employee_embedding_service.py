import os
import pandas as pd
import tiktoken
from openai import OpenAI
import pinecone

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")
PINECONE_INDEX_NAME = "productivity"
EMBEDDING_MODEL = "text-embedding-3-large"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
tokenizer = tiktoken.encoding_for_model(EMBEDDING_MODEL)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Ensure index exists
if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=3072,
        metric="cosine",
        spec=pinecone.ServerlessSpec(cloud="aws", region=PINECONE_REGION)
    )
index = pc.Index(PINECONE_INDEX_NAME)

def count_tokens(text):
    return len(tokenizer.encode(text))

def chunk_text(text, max_tokens=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    tokens = tokenizer.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk = tokenizer.decode(tokens[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap
    return chunks

def get_embedding(text):
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding

def store_to_pinecone(vector_id, embedding, metadata):
    index.upsert(vectors=[(str(vector_id), embedding, metadata)])

async def process_employee_csv_service(file_path: str):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["Story ID", "EmployeeID"])

    for idx, row in df.iterrows():
        # ✅ Normalize the keys of the row to remove trailing spaces
        row = {k.strip(): v for k, v in row.items()}

        story_id = str(row.get("Story ID", f"row{idx}")).strip()
        task = str(row.get("Task Name", "")).strip()
        project_type = str(row.get("Project Type", "")).strip()
        story_type = str(row.get("Story Type", "")).strip()
        point = str(row.get("Point", "")).strip()
        hours = str(row.get("Woking Hour(s)", "")).strip()
        status = str(row.get("Status", "")).strip()
        employee_id = str(row.get("EmployeeID", "")).strip()
        employee_name = str(row.get("Employee Name", "")).strip()

        #  Debug missing name if needed
        if not employee_name:
            print(f"[WARN] Missing employee name for row {idx} | EmployeeID: {employee_id}")

        #  Always store clean text for search accuracy
        text = (
            f"Employee Name: {employee_name} | "
            f"Employee ID: {employee_id} | "
            f"Task: {task} | "
            f"Project Type: {project_type} | "
            f"Story Type: {story_type} | "
            f"Points: {point} | "
            f"Hours: {hours} | "
            f"Status: {status}"
        )

        # ⛏️ Chunking if necessary
        chunks = chunk_text(text) if count_tokens(text) > CHUNK_SIZE else [text]

        for i, chunk in enumerate(chunks):
            chunk_id = f"{employee_id}_{story_id}_{i}" if len(chunks) > 1 else f"{employee_id}_{story_id}"
            embedding = get_embedding(chunk)
            metadata = {
                "employee_id": employee_id,
                "employee_name": employee_name,
                "story_id": story_id,
                "task_name": task,
                "project_type": project_type,
                "story_type": story_type,
                "point": point,
                "hours": hours,
                "status": status,
                "chunk_index": i,
                "text": text  #  Include full text in metadata
            }
            store_to_pinecone(chunk_id, embedding, metadata)

    return {"message": f"{len(df)} records embedded and stored."}
