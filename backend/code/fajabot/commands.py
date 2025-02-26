from datetime import timedelta

from playsound import playsound
from twitchAPI.chat import Chat
from twitchAPI.chat import ChatCommand

from fajabot import events
from fajabot.cooldown import cooldown
from fajabot.driver import get_profile
from fajabot.driver import update_profile
from fajabot.game import DefenceStage
from fajabot.game import FightResult
from fajabot.game import fight
from fajabot.profile import ProfileIdentity
from fajabot.quests import apply_quest
from fajabot.quests import draw_quest

TEXTS = {
    "intro": "Stwórz swoją !postac, rób !quest oraz !walcz z bossami. Rób questy, aby mieć lepszą broń lub pancerz. Walcz z bossami, aby zdobywać punkty. Masz tylko 4 życia więc uważaj. !topzywych oraz !topall aby zobaczyć topkę.",
    "profile": "@{name} ma {attack}/{defence} (atak/obrona) i {hp}hp. Doświadczenie: {experience}",
    "fight": "@{name} {profile_attack_base}+{profile_roll} walczy z goblinem {enemy_attack_base}+{enemy_roll}.",
    "profile_is_hit": "Goblin trafił i zadał 1hp.",
    "profile_is_not_hit": "Goblin trafił, ale nie zadał obrażeń.",
    "enemy_is_hit": "Trafiłeś i dostajes {exp}exp.",
    "enemy_is_not_hit": "Trafiłeś, ale nie zadałeś obrażeń.",
    "draw": "Potyczka nie została rozstrzygnięta (remis).",
    "death": "Twoja postać zginęła. :(",
    "waitforsound": "Poczekaj na dźwięk alertu.",
    "notimplemented": "Ta komenda jeszcze nie działa.",
    "commands": "!czatgra !postac !quest !walcz !topzywych !topall !strimujwiecej !komendy",
    "profile_not_found": "Ten użytkownik nie ma przypisanej postaci",
}

async def chatgra(cmd: ChatCommand):
    await cmd.send(TEXTS["intro"])
    await events.send_chatgra()


async def profilecmd(cmd: ChatCommand):
    texts = cmd.text.split(" ")
    while ' ' in texts:
        texts.remove(' ')
    if len(texts) == 1:
        profile = await get_profile(ProfileIdentity(cmd.user.name, cmd.room.name))
    else:
        name = texts[1]
        if name.startswith("@"):
            name = name[1:]
        profile = await get_profile(ProfileIdentity(name, cmd.room.name))
        if not profile:
            await cmd.reply(TEXTS["profile_not_found"])
            return
    text = TEXTS["profile"].format(
        name=cmd.user.name,
        attack=profile.attack,
        defence=profile.defence,
        hp=profile.hp,
        experience=profile.experience,
    )
    await cmd.reply(text)
    await events.send_profile(profile)

@cooldown("quest", timedelta(hours=1))
async def quest(cmd: ChatCommand):
    profile_id = ProfileIdentity(cmd.user.name, cmd.room.name)
    profile = await get_profile(profile_id)
    quest = draw_quest()
    await apply_quest(profile, quest)
    await cmd.reply(quest.text)


@cooldown("walcz", timedelta(hours=1))
async def walcz(cmd: ChatCommand):
    profile_id = ProfileIdentity(cmd.user.name, cmd.room.name)
    fight_log = await fight(profile_id)

    data = dict(
        name=cmd.user.name,
        profile_attack_base=fight_log.profile.attack,
        profile_roll=fight_log.stages[0].profile_attack - fight_log.profile.attack,
        enemy_attack_base=fight_log.enemy.attack,
        enemy_roll=fight_log.stages[0].enemy_attack - fight_log.enemy.attack,
    )
    texts = [TEXTS["fight"].format(**data)]
    defence_result = fight_log.stages[1]
    if defence_result.result == FightResult.profile_is_hit:
        texts.append(TEXTS["profile_is_hit"])
    elif defence_result.result == FightResult.profile_is_not_hit:
        texts.append(TEXTS["profile_is_not_hit"])
    elif defence_result.result == FightResult.enemy_is_hit:
        texts.append(TEXTS["enemy_is_hit"].format(exp=defence_result.profile_exp_change))
    elif defence_result.result == FightResult.enemy_is_not_hit:
        texts.append(TEXTS["enemy_is_not_hit"])
    else:
        texts.append(TEXTS["draw"])

    active = await update_profile_after_fight(
        profile_id,
        defence_result,
    )
    if not active:
        texts.append(TEXTS["death"])

    await events.send_fight(data, fight_log, active, texts)

    await cmd.send(" ".join(texts))


async def update_profile_after_fight(profile_id: ProfileIdentity, defence_result: DefenceStage):
    if defence_result.profile_hp_change == 0 and defence_result.profile_exp_change == 0:
        return True
    if defence_result.result == FightResult.draw:
        return True

    profile = await get_profile(profile_id)
    row_changes = {"active": True}
    if defence_result.profile_hp_change != 0:
        row_changes["hp"] = profile.hp + defence_result.profile_hp_change
        if row_changes["hp"] <= 0:
            row_changes["active"] = False
    if defence_result.profile_exp_change != 0:
        row_changes["experience"] = profile.experience + defence_result.profile_exp_change
    await update_profile(profile_id, **row_changes)
    return row_changes["active"]


async def topzywych(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


async def topall(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


@cooldown("strimmore", timedelta(hours=1))
async def strimmore(cmd: ChatCommand):
    playsound("/home/socek/Downloads/war2/WarCraft 2 Sounds/Wizard/Wzpissd1.wav")
    await cmd.reply(TEXTS["waitforsound"])


async def commands(cmd: ChatCommand):
    await cmd.reply(TEXTS["commands"])


def register(chat: Chat):
    chat.register_command("czatgra", chatgra)
    chat.register_command("postac", profilecmd)
    chat.register_command("quest", quest)
    chat.register_command("walcz", walcz)
    chat.register_command("topzywych", topzywych)
    chat.register_command("topall", topall)
    chat.register_command("strimujwiecej", strimmore)
    chat.register_command("komendy", commands)
