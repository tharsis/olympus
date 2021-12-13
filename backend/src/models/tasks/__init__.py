from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from src.database import Base


class TaskDb(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), index=True, unique=True)
    points = Column(Integer, default=0)

    def __repr__(self):
        return f'<Task {self.name}: {self.points}>'


class TaskSchema(BaseModel):
    name: str
    points: int
