from decouple import config
from twitchAPI.type import AuthScope

APP_ID = config("APP_ID")
APP_SECRET = config("APP_SECRET")
TARGET_CHANNEL = config("TARGET_CHANNEL")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]


def psql():
    name = config("POSTGRES_DB")
    user = config("POSTGRES_USER")
    password = config("POSTGRES_PASSWORD")
    host = config("POSTGRES_HOST")
    return f"postgresql+asyncpg://{user}:{password}@{host}:5432/{name}"


DB_URL: str = psql()
DB_OPTIONS: dict = {"pool_recycle": 3600, "pool_pre_ping": True}
