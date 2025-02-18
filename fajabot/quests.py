from dataclasses import dataclass
from datetime import timedelta
from random import choice
from typing import Optional

from fajabot.driver import set_cooldown
from fajabot.driver import update_profile
from fajabot.profile import Profile


@dataclass
class Quest:
    text: str
    probability: int = 1
    profile_hp_change: int = 0
    profile_defence_change: int = 0
    profile_attack_change: int = 0
    quest_cooldown: Optional[timedelta] = None
    fight_cooldown: Optional[timedelta] = None


quests = [
    Quest(
        "Wyszedłeś na wyprawę całkowicie uzbrojony i pełen nadziei. Ale nadzieja umiera ostatnia. Nic nie znalazłeś.",
        5,
    ),
    Quest(
        "Wyszedłeś na wyprawę. I znalazłeś butelke płynu. Wypijasz go. +1hp ty szczęściarzu/szczęściaro.",
        1,
        profile_hp_change=1,
    ),
    Quest(
        "Wyszedłeś na wyprawę. I znalazłeś butelke płynu. Wypijasz go. I się upijasz. Musisz poczekać, aż wytrzeźwiejesz. Polecam nie pić nieznanych i znalezionych płynów.",
        1,
        quest_cooldown=timedelta(hours=3),
        fight_cooldown=timedelta(hours=3),
    ),
    Quest(
        "Wkraczasz do lochu. Loch jest posępny i ciemny. Zanjdujesz nieznay płyn w butelce równie nieznanej. Wypijasz, bo jesteś aloholokiem. Okazało się, że to mocz. Smacznego. Straciłeś tylko trochę godności.",
        2,
    ),
    Quest(
        "Wkraczasz do lochu. Loch jest jasny, gdyż pomimo braku źródła światła, twórca gry dodał dużo światła. A na stole leży nowa, lepszy zbroja. +1 do obrony. Jest cała różowa.",
        1,
        profile_defence_change=1,
    ),
    Quest(
        "Zamiast iść na wyprawę postanowiłeś zostać w domu i wypucować swój miecz. +1 do ataku",
        1,
        profile_attack_change=1,
    ),
]


def draw_quest() -> Quest:
    quest_deck = []
    for quest in quests:
        for _ in range(quest.probability):
            quest_deck.append(quest)
    return choice(quest_deck)


def apply_quest(profile: Profile, quest: Quest):
    row_changes = {}
    if quest.profile_hp_change:
        row_changes["hp"] = profile.hp + quest.profile_hp_change
    if quest.profile_defence_change:
        row_changes["defence"] = profile.defence + quest.profile_defence_change
    if quest.profile_attack_change:
        row_changes["attack"] = profile.attack + quest.profile_attack_change

    update_profile(profile.user_id, **row_changes)

    if quest.quest_cooldown:
        set_cooldown(profile.user_id, "quest", quest.quest_cooldown)
    if quest.fight_cooldown:
        set_cooldown(profile.user_id, "quest", quest.fight_cooldown)
