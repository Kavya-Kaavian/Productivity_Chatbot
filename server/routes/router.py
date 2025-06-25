from fastapi import APIRouter, Query
from pydantic import BaseModel
from controller import *

router = APIRouter(prefix='/api', tags=['common_api'])

@router.get('/')
async def get_details():
    return await hello_world()