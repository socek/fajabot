from datetime import datetime
from datetime import timedelta
from typing import Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql import insert

from fajabot import settings
from fajabot.db.main import db
from fajabot.db.profile import CooldownTable
from fajabot.db.profile import ObsalertsTable
from fajabot.db.profile import ProfileTable
from fajabot.profile import Profile
from fajabot.profile import ProfileIdentity


def create_profile(
    user_id: ProfileIdentity,
    hp: int = 4,
    defence: int = 0,
    attack: int = 1,
):
    session = db()
    now = datetime.now()
    row = {
        "id": uuid4(),
        "user": user_id.user,
        "channel": user_id.channel,
        "hp": hp,
        "defence": defence,
        "attack": attack,
        "experience": 0,
        "active": True,
        "created_at": now,
        "updated_at": now,
    }
    rowcount = session.execute(insert(ProfileTable).values([row])).rowcount
    session.commit()
    return rowcount


def update_profile(
    user_id: ProfileIdentity,
    hp: Optional[int] = None,
    defence: Optional[int] = None,
    attack: Optional[int] = None,
    experience: Optional[int] = None,
    active: Optional[bool] = None,
):
    session = db()
    now = datetime.now()
    row = {
        "updated_at": now,
    }
    if hp is not None:
        row["hp"] = hp
    if defence is not None:
        row["defence"] = defence
    if attack is not None:
        row["attack"] = attack
    if experience is not None:
        row["experience"] = experience
    if active is not None:
        row["active"] = active

    session.query(ProfileTable.id).filter(
        ProfileTable.user == user_id.user,
        ProfileTable.channel == user_id.channel,
        ProfileTable.active == True,
    ).update(row)

    # TODO: upsert

    # find_response = (
    #     table.select("id")
    #     .eq("user", user_id.user)
    #     .eq("channel", user_id.channel)
    #     .eq("active", True)
    #     .execute()
    # )

    # if find_response.data == []:
    #     default_profile = {
    #         "hp": 4,
    #         "defence": 0,
    #         "attack": 1,
    #         "experience": 0,
    #         "active": True,
    #     }
    #     default_profile.update(row)
    #     response = table.insert(default_profile).execute()
    #     return
    # else:
    #     row_id = find_response.data[0]["id"]
    #     (table.update(row).eq("id", row_id).execute())
    #     return


def get_profile(user_id: ProfileIdentity, create_default: bool = True) -> Optional[Profile]:
    session = db()

    result = (
        session.query(
            ProfileTable.hp, ProfileTable.defence, ProfileTable.attack, ProfileTable.experience
        )
        .filter(
            ProfileTable.user == user_id.user,
            ProfileTable.channel == user_id.channel,
            ProfileTable.active == True,
        )
        .first()
    )

    profile = Profile(
        ProfileIdentity(user_id.user, user_id.channel),
    )
    if result:
        row = result._asdict()
        profile.hp = row["hp"]
        profile.defence = row["defence"]
        profile.attack = row["attack"]
        profile.experience = row["experience"]
        return profile
    elif create_default:
        return profile


def set_cooldown(user_id: ProfileIdentity, command: str, time: timedelta):
    session = db()
    row = {
        "id": uuid4(),
        "user": user_id.user,
        "channel": user_id.channel,
        "command": command,
        "cooldown": (datetime.now() + time).isoformat(),
    }
    rowcount = session.execute(insert(CooldownTable).values([row])).rowcount
    session.commit()
    return rowcount


def get_cooldown_time(user_id: ProfileIdentity, command: str) -> Optional[list]:
    session = db()

    result = (
        session.query(CooldownTable.cooldown)
        .filter(
            CooldownTable.user == user_id.user,
            CooldownTable.channel == user_id.channel,
            CooldownTable.command == command,
            CooldownTable.cooldown > datetime.now(),
        )
        .first()
    )

    if result:
        div = result[0] - datetime.now()
        return [div.days, div.seconds // 3600, div.seconds // 60 % 60, div.seconds % 3600 % 60]

def add_obs_event(payload: dict):
    session = db()
    row = {
        "id": uuid4(),
        "created_at": datetime.now(),
        "payload": payload
    }
    rowcount = session.execute(insert(ObsalertsTable).values([row])).rowcount
    session.commit()
    return rowcount

def get_obs_events(fromtime: datetime) -> list:
    session = db()
    result = session.query(
        ObsalertsTable.created_at,
        ObsalertsTable.payload,
    ).filter(
        ObsalertsTable.created_at > fromtime,
    )
    return [row._asdict() for row in result]
