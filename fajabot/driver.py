import os
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


def get_profile(user_id: ProfileIdentity, create_default: bool = True) -> Profile:
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
    if create_default and find_response.data != []:
        row = find_response.data[0]
        profile.hp = row["hp"]
        profile.defence = row["defence"]
        profile.attack = row["attack"]
        profile.experience = row["experience"]
    else:
        return None

    return profile
