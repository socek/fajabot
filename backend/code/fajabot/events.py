from dataclasses import asdict
from dataclasses import is_dataclass
from enum import Enum

from fajabot.driver import add_obs_event
from fajabot.game import FightLog
from fajabot.profile import Profile


async def send_chatgra():
    await add_obs_event({"event": "chatgra"})


async def send_profile(profile: Profile):
    profile = asdict(profile)
    profile["user"] = profile["user_id"]["user"]
    profile["channel"] = profile["user_id"]["channel"]
    del profile["user_id"]
    await add_obs_event({"event": "postac", "profile": profile})


async def send_fight(fight_data: dict, fight_log: FightLog, active: bool):
    fight_log = asdict(fight_log)
    for row in fight_log["stages"]:
        if "result" in row and is_dataclass(row["result"]):
            row["result"] = asdict(row["result"])
        if "result" in row and isinstance(row["result"], Enum):
            row["result"] = row["result"].name
    await add_obs_event(
        {
            "event": "fight",
            "fight_data": fight_data,
            "fight_log": fight_log,
            "active": active,
        }
    )
