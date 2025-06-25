from fastapi import APIRouter, Query
from pydantic import BaseModel

from controller.helloWorldController import hello_world


router = APIRouter(prefix='/api', tags=['common_api'])

@router.get('/')
async def get_details():
    return await hello_world()