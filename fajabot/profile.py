from dataclasses import dataclass


@dataclass
class ProfileIdentity:
    user: str
    channel: str


@dataclass
class Profile:
    user_id: ProfileIdentity
    hp: int
    defence: int
    attack: int
    experience: int
    active: bool = True
