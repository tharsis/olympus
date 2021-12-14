from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic.main import BaseModel
from sqlalchemy.orm import Session
from src.database import session_for_request
from src.database.tasks import get_all_tasks
from src.endpoints.constants import TASKS_TAG

router = APIRouter()


class Task(BaseModel):
    id: int
    name: str
    points: int


class Tasks(BaseModel):
    tasks: List[Task]


@router.get('/tasks', tags=[TASKS_TAG], response_model=Tasks)
async def tasks(db: Session = Depends(session_for_request)):
    ret = []
    for task in get_all_tasks(db):
        ret.append({'id': task.id, 'name': task.name, 'points': task.points})
    return {'tasks': ret}
