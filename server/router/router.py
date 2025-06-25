<<<<<<< HEAD
from fastapi import APIRouter, Query
from pydantic import BaseModel

from controller.helloWorldController import hello_world

=======
from fastapi import APIRouter, UploadFile,Query
from pydantic import BaseModel
from controller.employee_controller import process_csv_controller
from controller.retriever_controller import search_controller
import shutil
import os
>>>>>>> 4705b3c242d1911be907d78cc8efbdab5fee923d

router = APIRouter(prefix='/api', tags=['common_api'])

@router.get('/')
async def get_details():
<<<<<<< HEAD
    return await hello_world()
=======
    return await hello_world()

@router.post("/upload")
async def upload_csv(file: UploadFile):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return await process_csv_controller(file_path)


# Define the request model
class SearchRequest(BaseModel):
    query: str

@router.post("/search")
async def search_endpoint(
    body: SearchRequest,
    top_k: int = Query(5)
):
    return await search_controller(body.query, top_k)
>>>>>>> 4705b3c242d1911be907d78cc8efbdab5fee923d
