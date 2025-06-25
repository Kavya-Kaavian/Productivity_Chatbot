from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from services.assistant_service import call_assistant
import httpx

async def handle_assistant_request(request: Request):
    body = await request.json()
    question = body.get("question")

    if not question:
        raise HTTPException(status_code=400, detail="Missing question")

    # Step 1: Fetch context from external API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8000/api/fetch-data", json={"question": question})
            response.raise_for_status()
            context = response.json().get("context", "")
    except Exception as e:
        print(f"Error fetching context: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch context")

    # Step 2: Set static prompt
    prompt = """
    You are an intelligent productivity assistant.

    Provide brief, data-driven responses to user questions, maintaining a concise and professional tone.

    Guidelines:
    - Summarize only the most relevant data.
    - Keep answers short and to the point (1-2 short paragraphs).
    - Avoid lengthy explanations or detailed breakdowns.
    - Highlight only the most relevant employee(s) or tasks based on the question.
    - For questions involving lists (e.g., "list out", "suggest"), return the final answer in a clear list format.
    - For greetings or thank-you messages, respond politely (e.g., “Hello, how can I assist you today?” or “You're welcome! How else may I help?”).
    - If the question is unrelated to the context, respond with: “I'm not sure about that, please ask me something else.”
    - If the question is empty, respond with: “Please ask me a question.”

    Stay focused and helpful.
    """

    # Step 3: Call Assistant
    if(context == ""):
        return JSONResponse(content={"answer": "I'm not sure about that, please ask me something else."})
    try:
        answer = await call_assistant(question, context, prompt)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        print(f"Assistant Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process assistant request")
