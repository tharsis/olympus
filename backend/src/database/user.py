from sqlalchemy.orm import Session
from src.models.users import UserDb


def get_user_by_id(db: Session, id: int):
    res = db.query(UserDb).filter(UserDb.id == id).first()
    if res is not None:
        return True, res
    return False, res
