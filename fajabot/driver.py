from typing import Optional

from fajabot.profile import Profile
from fajabot.profile import ProfileIdentity


def create_profile(user_id: ProfileIdentity, hp: int, defence: int, attack: int):
    pass


def update_profile(
    user_id: ProfileIdentity,
    hp: Optional[int],
    defence: Optional[int],
    attack: Optional[int],
    experience: Optional[int],
    active: Optional[bool] = None,
):
    pass


def get_profile(user_id: ProfileIdentity) -> Profile:
    return Profile(ProfileIdentity("socek", "#chan"), 4, 0, 1, 0)
