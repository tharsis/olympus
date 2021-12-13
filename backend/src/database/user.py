from sqlalchemy.orm import Session
from src.models.completed import CompletedDb
from src.models.users import UserDb


def get_user_by_id(db: Session, id: int):
    res = db.query(UserDb).filter(UserDb.id == id).first()
    if res is not None:
        return True, res
    return False, None


def get_user_missions_by_wallet(db: Session, wallet: str):
    res = []
    user = db.query(UserDb).filter(UserDb.wallet == wallet).first()
    if user is not None:
        missions = db.query(CompletedDb).filter(CompletedDb.id_user == user.id).all()
        for m in missions:
            res.append(m.id_task)
        return True, res
    return False, res
