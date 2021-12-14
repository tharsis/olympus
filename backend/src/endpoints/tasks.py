from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic.main import BaseModel
from sqlalchemy.orm import Session
from src.database import session_for_request
from src.database.tasks import get_all_tasks
from src.endpoints.constants import TASKS_TAG
from src.models.completed import CompletedDb

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


class Completed(BaseModel):
    wallet: str
    missions: List[int]


class CompletedTasks(BaseModel):
    completed: List[Completed]


@router.get('/get_all_completed_tasks', tags=[TASKS_TAG], response_model=CompletedTasks)
async def get_all_completed_tasks(db: Session = Depends(session_for_request)):
    res = []
    missions = db.query(CompletedDb).order_by(CompletedDb.id_user).all()
    current_user_id = None
    current_user_name = None
    temp = []
    for m in missions:
        if m.id_user != current_user_id:
            if temp != []:
                res.append({'wallet': current_user_name, 'missions': temp})
                temp = []
            current_user_id = m.id_user
            current_user_name = m.completed.wallet
            temp.append(m.id_task)
        else:
            temp.append(m.id_task)
    if temp != []:
        res.append({'wallet': current_user_name, 'missions': temp})
    return {'completed': res}
