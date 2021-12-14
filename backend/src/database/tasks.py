from sqlalchemy.orm import Session
from src.models.tasks import TaskDb


def get_all_tasks(db: Session):
    return db.query(TaskDb).all()
