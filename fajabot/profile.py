from dataclasses import dataclass


@dataclass
class ProfileIdentity:
    user: str
    channel: str


@dataclass
class Profile:
    user_id: ProfileIdentity
    hp: int = 4
    defence: int = 0
    attack: int = 1
    experience: int = 0
    active: bool = True
