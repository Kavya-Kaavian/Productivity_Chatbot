from fastapi import APIRouter, Request

from controller.assistant_controller import handle_assistant_request


router = APIRouter()

@router.post("/ask")
async def ask(request: Request):
    return await handle_assistant_request(request)
