from datetime import datetime
from datetime import timedelta
from typing import Optional
from uuid import uuid4

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fajabot.db.main import transaction
from fajabot.db.profile import CooldownTable
from fajabot.db.profile import KVStoreTable
from fajabot.db.profile import ObsalertsTable
from fajabot.db.profile import ProfileTable
from fajabot.profile import Profile
from fajabot.profile import ProfileIdentity

AUTH_TOKEN_KEY = "auth_token"


@transaction
async def create_profile(
    user_id: ProfileIdentity,
    hp: int = 4,
    defence: int = 0,
    attack: int = 1,
    session: AsyncSession = None,
):
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
    stmt = insert(ProfileTable).values([row])
    return (await session.execute(stmt)).rowcount


@transaction
async def update_profile(
    user_id: ProfileIdentity,
    hp: Optional[int] = None,
    defence: Optional[int] = None,
    attack: Optional[int] = None,
    experience: Optional[int] = None,
    active: Optional[bool] = None,
    session: AsyncSession = None,
):
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

    stmt = select(ProfileTable.id).filter(
        ProfileTable.user == user_id.user,
        ProfileTable.channel == user_id.channel,
        ProfileTable.active == True,
    )
    result = (await session.execute(stmt)).first()

    if result:
        stmt = update(ProfileTable).where(ProfileTable.id == result[0]).values(row)
        await session.execute(stmt)
    else:
        insert_row = dict(**row)
        insert_row["id"] = uuid4()
        insert_row["user"] = user_id.user
        insert_row["channel"] = user_id.channel
        insert_row["created_at"] = now
        insert_row["active"] = True
        stmt = insert(ProfileTable).values([insert_row])
        await session.execute(stmt)


@transaction
async def get_profile(
    user_id: ProfileIdentity,
    create_default: bool = True,
    session: AsyncSession = None,
) -> Optional[Profile]:
    stmt = (
        select(
            ProfileTable.hp, ProfileTable.defence, ProfileTable.attack, ProfileTable.experience
        )
        .filter(
            ProfileTable.user == user_id.user,
            ProfileTable.channel == user_id.channel,
            ProfileTable.active == True,
        )
    )
    result = (await session.execute(stmt)).first()

    profile = Profile(
        ProfileIdentity(user_id.user, user_id.channel),
    )
    if result:
        row = result._asdict()
        profile.hp = row.get("hp") or profile.hp
        profile.defence = row.get("defence") or profile.defence
        profile.attack = row.get("attack") or profile.attack
        profile.experience = row.get("experience") or profile.experience
        return profile
    elif create_default:
        return profile


@transaction
async def set_cooldown(
    user_id: ProfileIdentity,
    command: str,
    time: timedelta,
    session: AsyncSession = None,
):
    row = {
        "id": uuid4(),
        "user": user_id.user,
        "channel": user_id.channel,
        "command": command,
        "cooldown": datetime.now() + time,
    }
    stmt = insert(CooldownTable).values([row])
    return (await session.execute(stmt)).rowcount


@transaction
async def get_cooldown_time(
    user_id: ProfileIdentity,
    command: str,
    session: AsyncSession = None,
) -> Optional[list]:
    stmt = (
        select(CooldownTable.cooldown)
        .filter(
            CooldownTable.user == user_id.user,
            CooldownTable.channel == user_id.channel,
            CooldownTable.command == command,
            CooldownTable.cooldown > datetime.now(),
        )

    )
    result = (await session.execute(stmt)).first()

    if result:
        div = result[0] - datetime.now()
        return [div.days, div.seconds // 3600, div.seconds // 60 % 60, div.seconds % 3600 % 60]


@transaction
async def add_obs_event(
    payload: dict,
    session: AsyncSession = None,
):
    row = {"id": uuid4(), "created_at": datetime.now(), "payload": payload}
    stmt = insert(ObsalertsTable).values([row])
    return (await session.execute(stmt)).rowcount


def prepare_element(row):
    data = row._asdict()
    data["created_at"] = data["created_at"].isoformat()
    return data


@transaction
async def get_obs_events(
    fromtime: datetime,
    session: AsyncSession = None,
) -> list:
    stmt = select(
        ObsalertsTable.created_at,
        ObsalertsTable.payload,
    ).filter(
        ObsalertsTable.created_at > fromtime,
    )
    result = await session.execute(stmt)
    return [prepare_element(row) for row in result]


@transaction
async def set_auth_tokens(
    token: str,
    refresh_token: str,
    session: AsyncSession = None,
):
    payload = {
        "token": token,
        "refresh_token": refresh_token,
    }
    stmt = insert(KVStoreTable).values(
        key=AUTH_TOKEN_KEY,
        payload=payload,
        updated_at=datetime.now(),
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=[KVStoreTable.key],
        index_where=KVStoreTable.key == AUTH_TOKEN_KEY,
        set_=dict(
            payload=payload,
            updated_at=datetime.now(),
        ),
    )
    await session.execute(stmt)


@transaction
async def get_auth_tokens(session: AsyncSession = None):
    stmt = (
        select(
            KVStoreTable.payload,
        )
        .filter(
            KVStoreTable.key == AUTH_TOKEN_KEY,
        )
    )
    result = (await session.execute(stmt)).first()

    if result:
        row = result[0]
        return row["token"], row["refresh_token"]
    else:
        return "", ""
