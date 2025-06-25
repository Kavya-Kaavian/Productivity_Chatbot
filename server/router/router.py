from fastapi import APIRouter, UploadFile,Query
from controller.employee_controller import process_csv_controller
from controller.retriever_controller import search_controller
import shutil
import os

router = APIRouter(prefix='/api', tags=['common_api'])

@router.get('/')
async def get_details():
    return await hello_world()

@router.post("/upload")
async def upload_csv(file: UploadFile):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return await process_csv_controller(file_path)

@router.get("/search")
async def search(
    query: str = Query(...),
    top_k: int = Query(5),
):
    return await search_controller(query, top_k)