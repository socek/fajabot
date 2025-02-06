from dataclasses import dataclass
from dataclasses import field
from random import randint
from typing import Optional

from fajabot.driver import get_profile
from fajabot.profile import Profile
from fajabot.profile import ProfileIdentity

RANGE = 3
ROLL = 6


@dataclass
class Enemy:
    defence: int
    attack: int


@dataclass
class FightStage:
    name: str


@dataclass
class ClashStage(FightStage):
    name: str = field(init=False)
    enemy_attack: int
    profile_attack: int

    def __post_init__(self):
        self.name = "clash"

    def result(self):
        if self.profile_attack > self.enemy_attack:
            return "profile_win"
        elif self.profile_attack < self.enemy_attack:
            return "enemy_win"
        else:
            return "draw"


@dataclass
class DefenceStage(FightStage):
    name: str = field(init=False)
    result: str
    profile_hp_change: int = 0
    profile_exp_change: int = 0

    def __post_init__(self):
        self.name = "defence"


@dataclass
class FightLog:
    profile: Optional[Profile] = None
    enemy: Optional[Enemy] = None
    stages: list[FightStage] = field(default_factory=list)


def _create_enemy(defence: int, attack: int) -> Enemy:
    defence = randint(RANGE * -1, RANGE) + defence
    if defence < 0:
        defence = 0

    attack = randint(RANGE * -1, RANGE) + attack
    if attack < 1:
        attack = 1

    return Enemy(defence, attack)


def fight(user_id: ProfileIdentity):
    profile = get_profile(user_id)
    enemy = _create_enemy(profile.defence, profile.attack)
    fight_log = FightLog(profile, enemy)

    clash = clash_stage(profile, enemy)
    fight_log.stages.append(clash)

    defence = defence_stage(profile, enemy, clash)
    fight_log.stages.append(defence)

    return fight_log


def clash_stage(profile: Profile, enemy: Enemy) -> ClashStage:
    profile_attack = randint(1, ROLL) + profile.attack
    enemy_attack = randint(1, ROLL) + enemy.attack
    return ClashStage(enemy_attack=enemy_attack, profile_attack=profile_attack)


def defence_stage(profile, enemy, clash: ClashStage):
    if clash.result() == "profile_win":
        if clash.profile_attack > enemy.defence:
            return DefenceStage(result="enemy_is_hit", profile_exp_change=enemy.attack + enemy.defence)
        else:
            return DefenceStage(result="enemy_is_not_hit")
    elif clash.result() == "enemy_win":
        if clash.enemy_attack > profile.defence:
            return DefenceStage(result="profile_is_hit", profile_hp_change=-1)
        else:
            return DefenceStage(result="profile_is_not_hit")
    else:
        return DefenceStage(result="nothing")
