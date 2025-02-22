from datetime import datetime
from datetime import timedelta
from functools import wraps

from twitchAPI.chat import ChatCommand

from fajabot.driver import get_cooldown_time
from fajabot.driver import get_profile
from fajabot.driver import set_cooldown
from fajabot.profile import ProfileIdentity


def cooldown(command: str, cooldown_time: timedelta):
    def cooldown_configuration(fun):
        @wraps(fun)
        async def wrapper(cmd: ChatCommand, *args, **kwargs):
            user_id = ProfileIdentity(cmd.user.name, cmd.room.name)
            cooldown = get_cooldown_time(user_id, command)
            if cooldown:
                texts = []
                if cooldown[0]:
                    texts.append(f"{cooldown[0]} dni")
                if cooldown[1]:
                    texts.append(f"{cooldown[1]} godzin")
                if cooldown[2]:
                    texts.append(f"{cooldown[2]} minut")
                if cooldown[3]:
                    texts.append(f"{cooldown[3]} sekund")
                fulltext = f"Komenda odpoczywa jeszcze przez {' '.join(texts)}"
                await cmd.reply(fulltext)
            else:
                result = await fun(cmd, *args, **kwargs)
                set_cooldown(user_id, command, cooldown_time)
                return result

        return wrapper

    return cooldown_configuration
