# FastAPI Packages
from fastapi import FastAPI
from src.storage import storage_router

app = FastAPI(title="truShot", version="0.0.1+1")

app.include_router(storage_router)