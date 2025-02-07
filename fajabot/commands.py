from playsound import playsound
from twitchAPI.chat import Chat
from twitchAPI.chat import ChatCommand

from fajabot.driver import get_profile
from fajabot.game import FightResult
from fajabot.game import fight
from fajabot.profile import ProfileIdentity

TEXTS = {
    "intro": "Stwórz swoją !postac, rób !quest oraz !walcz z bossami. Rób questy, aby mieć lepszą broń lub pancerz. Walcz z bossami, aby zdobywać punkty. Masz tylko 4 życia więc uważaj. !topzywych oraz !topall aby zobaczyć topkę.",
    "postać": "@{name} Masz {attack}/{defence} (atak/obrona) i {hp}hp. Twój exp: {experience}",
    "fight": "@{name} {profile_attack_base}+{profile_attack} walczy z goblinem {enemy_attack_base}+{enemy_attack}.",
    "profile_is_hit": "Goblin trafił i zadał 1hp.",
    "profile_is_not_hit": "Goblin trafił, ale nie zadał obrażeń.",
    "enemy_is_hit": "Trafiłeś i dostajes {exp}exp.",
    "enemy_is_not_hit": "Trafiłeś, ale nie zadałeś obrażeń.",
    "draw": "Potyczka nie została rozstrzygnięta (remis).",
    "waitforsound": "Poczekaj na dźwięk alertu.",
    "notimplemented": "Ta komenda jeszcze nie działa.",
    "commands": "!czatgra !postac !quest !walcz !topzywych !topall !strimujwiecej !komendy",
}


async def chatgra(cmd: ChatCommand):
    ic("chatgra")
    await cmd.send(TEXTS["intro"])
    playsound("/home/socek/Downloads/war2/WarCraft 2 Sounds/Misc/Ocapture.wav")


async def postac(cmd: ChatCommand):
    ic("postac", cmd.text)
    profile = get_profile(ProfileIdentity(cmd.user.id, cmd.room.name))
    text = TEXTS["postać"].format(
        name=cmd.user.name,
        attack=profile.attack,
        defence=profile.defence,
        hp=profile.hp,
        experience=profile.experience,
    )
    await cmd.reply(text)
    playsound("/home/socek/Downloads/war2/WarCraft 2 Sounds/Misc/Pig.wav")


async def quest(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


async def walcz(cmd: ChatCommand):
    ic("Walcz")
    profile_id = ProfileIdentity(cmd.user.id, cmd.room.name)
    fight_log = fight(profile_id)

    texts = [
        TEXTS["fight"].format(
            name=cmd.user.name,
            profile_attack_base=fight_log.profile.attack,
            profile_attack=fight_log.stages[0].profile_attack,
            enemy_attack_base=fight_log.enemy.attack,
            enemy_attack=fight_log.stages[0].enemy_attack,
        )
    ]
    defence_result = fight_log.stages[1]
    ic(defence_result, defence_result.result)
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

    await cmd.send(" ".join(texts))
    playsound("/home/socek/Downloads/war2/WarCraft 2 Sounds/Misc/Sword2.wav")


async def topzywych(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


async def topall(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


async def strimmore(cmd: ChatCommand):
    playsound("/home/socek/Downloads/war2/WarCraft 2 Sounds/Wizard/Wzpissd1.wav")
    await cmd.reply(TEXTS["waitforsound"])


async def commands(cmd: ChatCommand):
    await cmd.reply(TEXTS["commands"])


def register(chat: Chat):
    chat.register_command("czatgra", chatgra)
    chat.register_command("postac", postac)
    chat.register_command("quest", quest)
    chat.register_command("walcz", walcz)
    chat.register_command("topzywych", topzywych)
    chat.register_command("topall", topall)
    chat.register_command("strimujwiecej", strimmore)
    chat.register_command("komendy", commands)
