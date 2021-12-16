from fastapi import FastAPI
from src.endpoints.blockchain import router as blockchain_router
from src.endpoints.tasks import router as tasks_router
from src.endpoints.user import router as user_router


def add_routes(app: FastAPI):
    app.include_router(user_router)
    app.include_router(tasks_router)
    app.include_router(blockchain_router)
