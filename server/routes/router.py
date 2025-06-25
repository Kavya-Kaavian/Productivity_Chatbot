from fastapi import APIRouter, Query
from pydantic import BaseModel
from controller import *

router = APIRouter(prefix='/api', tags=['common_api'])

@router.get('/')
async def get_details():
    return await hello_world()

class QueryVectorRequest(BaseModel):
    query: str

@router.post('/fetch-data')
async def fetchData(data: QueryVectorRequest):
    return await getDataFromDb(data.query)


 