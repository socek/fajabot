from contextvars import ContextVar
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from fajabot.settings import DB_OPTIONS
from fajabot.settings import DB_URL

_engine_cache = ContextVar("engine")


async def _engine():
    if not _engine_cache.get(None):
        _engine_cache.set(create_async_engine(DB_URL, **DB_OPTIONS))
    return _engine_cache.get(None)


async def db():
    return AsyncSession(await _engine(), expire_on_commit=False)


def transaction(fun):
    @wraps(fun)
    async def wrapper(*args, **kwargs):
        session = await db()
        async with session.begin():
            res = await fun(*args, session=session, **kwargs)
            await session.commit()
        return res

    return wrapper
