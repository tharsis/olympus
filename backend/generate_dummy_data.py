from random import randrange

from sqlalchemy.sql.expression import and_
from src.database import internal_session
from src.models.completed import CompletedDb
from src.models.tasks import TaskDb
from src.models.users import UserDb

with internal_session() as session:
    for i in range(10):
        session.add(TaskDb(name=f'TaskNumber{i+1}', points=randrange(30)))
    for i in range(1000):
        session.add(UserDb(wallet=f'wallet{i}'))

    session.commit()
    session.flush()

    for i in range(8000):
        id_user = randrange(999) + 1
        id_task = randrange(9) + 1
        res = session.query(CompletedDb).filter(and_(CompletedDb.id_user == id_user,
                                                     CompletedDb.id_task == id_task)).first()
        if res is None:
            session.add(CompletedDb(id_user=id_user, id_task=id_task))

    session.flush()
