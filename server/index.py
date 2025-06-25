import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.router import *

app = FastAPI()

origin = os.getenv("ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins =origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)