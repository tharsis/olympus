from fastapi import FastAPI
from src.endpoints.user import router as user_router


def add_routes(app: FastAPI):
    app.include_router(user_router)
