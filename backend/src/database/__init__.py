import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', ) or 'postgresql+pg8000://postgres:U6bwFSLqmBVU90CWwDuRFYL8aiHA_crkuphxZLqw@127.0.0.1:5432'
POOL_SIZE = 10
MAX_OVERFLOW = 10

engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=POOL_SIZE, max_overflow=MAX_OVERFLOW)

Session = sessionmaker(bind=engine)

Base = declarative_base()


def session_for_request(callback=None):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        if callback is not None:
            callback()
    finally:
        session.close()


@contextmanager
def internal_session():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
