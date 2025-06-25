import os
import pandas as pd
import openai
import pinecone
import tiktoken
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Init OpenAI & Pinecone
openai.api_key = os.getenv("OPEN_AI_KEY")
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")

tokenizer = tiktoken.encoding_for_model(EMBEDDING_MODEL)



# === Chunking Settings ===
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

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
    response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response["data"][0]["embedding"]

def store_to_pinecone(vector_id, embedding, metadata):
    index.upsert([(str(vector_id), embedding, metadata)])
    print(f"✅ Stored in Pinecone: {vector_id}")

def process_employee_excel(file_path):
    # Load top 2 rows for metadata
    top_meta = pd.read_excel(file_path, header=None, nrows=2)
    employee_id = str(top_meta.iloc[0, 1]).strip()
    employee_name = str(top_meta.iloc[1, 1]).strip()

    # Load task data starting from row 3
    df = pd.read_excel(file_path, header=2)
    df = df.dropna(subset=["Story ID"])  # Skip summary rows

    print(f"\n👤 Processing Employee: {employee_id} - {employee_name}")
    print(f"📊 Total tasks: {len(df)}")

    for idx, row in df.iterrows():
        story_id = str(row.get("Story ID", f"row{idx}")).strip()
        task = str(row.get("Story Name / Task Name", "")).strip()
        project_type = str(row.get("Project Type", "")).strip()
        story_type = str(row.get("Story Type", "")).strip()
        point = str(row.get("Point", "")).strip()
        hours = str(row.get("Woking Hour(s)", "")).strip()
        status = str(row.get("Status", "")).strip()

        full_text = f"{task} | Project Type: {project_type} | Story Type: {story_type} | Points: {point} | Hours: {hours} | Status: {status}"

        chunks = chunk_text(full_text) if count_tokens(full_text) > CHUNK_SIZE else [full_text]

        for i, chunk in enumerate(chunks):
            chunk_id = f"{story_id}_{i}" if len(chunks) > 1 else story_id
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
                "chunk_index": i
            }

            store_to_pinecone(chunk_id, embedding, metadata)

if __name__ == "__main__":
    process_employee_excel("vishvadata.xlsx")
