from decouple import config
from twitchAPI.type import AuthScope

APP_ID = config("APP_ID")
APP_SECRET = config("APP_SECRET")
TARGET_CHANNEL = config("TARGET_CHANNEL")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

SUPABASE_URL: str = config("SUPABASE_URL")
SUPABASE_KEY: str = config("SUPABASE_KEY")
