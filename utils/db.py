from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import sessionmaker
from utils.config import config

_engine = None
_metadata = None
Session = None


def get_engine():
    global _engine
    if not _engine:
        _engine = create_engine(
            config['DATABASE_URL'],
            echo=config['DATABASE_DEBUG']
        )
    return _engine


def get_metadata():
    global _metadata
    if not _metadata and _engine:
        _metadata = MetaData(bind=_engine)
        _metadata.reflect()

    return _metadata


def get_session_maker():
    global Session
    if not Session and _engine:
        Session = sessionmaker(bind=_engine)

    return Session


def create_session():
    if not Session:
        get_session_maker()
    return Session()


def init_db():
    if not _engine:
        get_engine()
    if not _metadata:
        get_metadata()
    if not Session:
        get_session_maker()

    return True
