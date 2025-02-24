from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from fajabot.settings import DB_OPTIONS
from fajabot.settings import DB_URL

_CACHE = {}


def _engine():
    if not _CACHE.get("engine"):
        _CACHE["engine"] = create_async_engine(DB_URL, **DB_OPTIONS)
    return _CACHE["engine"]


def db():
    return AsyncSession(_engine(), expire_on_commit=False)

def transaction(fun):
    @wraps(fun)
    async def wrapper(*args, **kwargs):
        session = db()
        async with session.begin():
            res = await fun(*args, session=session, **kwargs)
            await session.commit()
        return res

    return wrapper
