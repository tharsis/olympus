from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.sql.schema import ForeignKey
from src.database import Base


class CompletedDb(Base):
    __tablename__ = 'completed'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'), index=True)
    id_task = Column(Integer, ForeignKey('task.id'), index=True)

    def __repr__(self):
        return f'<Completed {self.id_user}: {self.id_task}>'
