from sqlalchemy.orm import Session

from backend.src.models.tasks import TaskDb


def get_all_tasks(db: Session):
    return db.query(TaskDb).all()
