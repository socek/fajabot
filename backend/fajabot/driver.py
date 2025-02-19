from datetime import datetime
from datetime import timedelta
from typing import Optional

from supabase import Client
from supabase import create_client

from fajabot import settings
from fajabot.profile import Profile
from fajabot.profile import ProfileIdentity


def create_profile(
    user_id: ProfileIdentity,
    hp: int = 4,
    defence: int = 0,
    attack: int = 1,
):
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    row = {
        "user": user_id.user,
        "channel": user_id.channel,
        "hp": hp,
        "defence": defence,
        "attack": attack,
        "experience": 0,
    }
    supabase.table("profiles").insert(row).execute()


def update_profile(
    user_id: ProfileIdentity,
    hp: Optional[int] = None,
    defence: Optional[int] = None,
    attack: Optional[int] = None,
    experience: Optional[int] = None,
    active: Optional[bool] = None,
):
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    table = supabase.table("profiles")
    row = {
        "user": user_id.user,
        "channel": user_id.channel,
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

    find_response = (
        table.select("id")
        .eq("user", user_id.user)
        .eq("channel", user_id.channel)
        .eq("active", True)
        .execute()
    )
    if find_response.data == []:
        default_profile = {
            "hp": 4,
            "defence": 0,
            "attack": 1,
            "experience": 0,
            "active": True,
        }
        default_profile.update(row)
        response = table.insert(default_profile).execute()
        return
    else:
        row_id = find_response.data[0]["id"]
        (table.update(row).eq("id", row_id).execute())
        return


def get_profile(user_id: ProfileIdentity, create_default: bool = True) -> Optional[Profile]:
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    table = supabase.table("profiles")

    find_response = (
        table.select()
        .eq("user", user_id.user)
        .eq("channel", user_id.channel)
        .eq("active", True)
        .execute()
    )
    profile = Profile(
        ProfileIdentity(user_id.user, user_id.channel),
    )
    if find_response.data != []:
        row = find_response.data[0]
        profile.hp = row["hp"]
        profile.defence = row["defence"]
        profile.attack = row["attack"]
        profile.experience = row["experience"]
        return profile
    elif create_default:
        return profile


def set_cooldown(user_id: ProfileIdentity, command: str, time: timedelta):
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    row = {
        "user": user_id.user,
        "channel": user_id.channel,
        "command": command,
        "cooldown": (datetime.now() + time).isoformat(),
    }
    supabase.table("cooldowns").insert(row).execute()


def get_cooldown_time(user_id: ProfileIdentity, command: str) -> Optional[list]:
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    table = supabase.table("cooldowns")

    find_response = (
        table.select("cooldown")
        .eq("user", user_id.user)
        .eq("channel", user_id.channel)
        .eq("command", command)
        .gt("cooldown", datetime.now().isoformat())
        .execute()
    )
    if find_response.data != []:
        div = datetime.fromisoformat(find_response.data[0]["cooldown"]) - datetime.now()
        return [div.days, div.seconds // 3600, div.seconds // 60 % 60, div.seconds % 3600 % 60]

def get_obs_events(fromtime: datetime) -> list:
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    table = supabase.table("obsalerts")
    result = table.select("payload").gt("created_at", fromtime).execute()
    return [row["payload"] for row in result.data]
