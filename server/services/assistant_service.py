import time
from utils.openai_client import openai_client
import os

ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

async def call_assistant(question: str, context: str, prompt: str) -> str:
    # Step 1: Create a new thread
    thread = openai_client.beta.threads.create()

    # Step 2: Add combined message
    full_message = f"""{prompt}

Here is the context:
{context}

User's question:
{question}
"""

    openai_client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=full_message.strip()
    )

    # Step 3: Run the assistant
    run = openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Step 4: Poll for result
    while True:
        run_status = openai_client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        if run_status.status == "completed":
            break
        time.sleep(2)

    # Step 5: Get the assistant's final message
    messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value

    return "No response received from assistant."
