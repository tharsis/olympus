from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from src.database import Base


class UserDb(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    wallet = Column(String(120), index=True, unique=True)
    total_points = Column(Integer, default=0)

    user = relationship('CompletedDb', backref='completed', lazy=True)

    def __repr__(self):
        return f'<User {self.wallet}: {self.total_points}>'


class UserSchema(BaseModel):
    wallet: str
    totalPoints: int
