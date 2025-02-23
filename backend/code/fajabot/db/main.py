from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from fajabot.settings import DB_OPTIONS
from fajabot.settings import DB_URL

_CACHE = {}


def _engine():
    if not _CACHE.get("engine"):
        _CACHE["engine"] = create_engine(DB_URL, **DB_OPTIONS)
    return _CACHE["engine"]


def _sessionmaker():
    if not _CACHE.get("sessionmaker"):
        _CACHE["sessionmaker"] = sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=_engine(),
        )
    return _CACHE["sessionmaker"]


def db():
    return _sessionmaker()()
