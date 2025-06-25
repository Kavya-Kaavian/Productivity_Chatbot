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
            response = await client.post("http://localhost:8000/api/search?top_k=5", json={"query": question})
            response.raise_for_status()
            matches = response.json().get("matches", "")
    except Exception as e:
        print(f"Error fetching context: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch context")

    # Step 2: Set static prompt
    prompt = """
    You are a smart productivity assistant designed for Kaavian Systems.

Your job is to analyze employee productivity data and respond to questions with sharp, precise, and helpful answers. You are given structured context (such as task name, story type, project type, hours worked, and employee details). Use this to extract and present only the most relevant insights.

Guidelines:
- Provide brief, professional, and data-backed responses (1-2 short paragraphs).
- Highlight only the most relevant employee(s), tasks, or data based on the question.
- If asked for a list (e.g. "suggest", "list", "who are"), respond with a clear, clean list format.
- Greet the user politely for casual questions or greetings (e.g. “Hi”, “Thank you”).
- If the question is unrelated to the context (e.g. asking about sports, weather, etc.), respond with: “I'm not sure about that, please ask me something related to productivity.”
- If no question is provided, reply with: “Please ask me a question.”
- Avoid unnecessary elaboration, stay on-topic, and be office-appropriate.

Example:
**Question**: Who is doing the most UI work?
**Answer**: Based on the data, KAVN1610 has completed multiple UI-related tasks with a total of 4 points across 34 working hours. This employee stands out in frontend contributions.

Stay helpful, respectful, and relevant.

    """
    print(f"Received question: {matches}")
    # Step 3: Call Assistant
    if(matches == ""):
        return JSONResponse(content={"answer": "I'm not sure about that, please ask me something else."})
    try:
        answer = await call_assistant(question, matches, prompt)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        print(f"Assistant Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process assistant request")
