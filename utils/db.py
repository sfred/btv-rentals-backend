from sqlalchemy import (
    create_engine,
    MetaData
)
from utils.config import config

_engine = None
_metadata = None


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
    if not _metadata:
        _metadata = MetaData()

    return _metadata


def load_schema():
    if not _metadata:
        get_metadata()
    if not _engine:
        get_engine()

    _metadata.create_all(_engine)
    return True
