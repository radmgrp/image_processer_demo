from fastapi import FastAPI
from api.service import router
from starlette.middleware.cors import CORSMiddleware
import os

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/api/v1")
