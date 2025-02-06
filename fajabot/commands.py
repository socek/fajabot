from playsound import playsound
from twitchAPI.chat import Chat
from twitchAPI.chat import ChatCommand

from fajabot.driver import get_profile
from fajabot.profile import ProfileIdentity

TEXTS = {
    "intro": "Stwórz swoją !postac, rób !quest oraz !walcz z bossami. Rób questy, aby mieć lepszą broń lub pancerz. Walcz z bossami, aby zdobywać punkty. Masz tylko 4 życia więc uważaj. !topzywych oraz !topall aby zobaczyć topkę.",
    "postać": "@{name} Masz {attack}/{defence} (atak/obrona) i {hp}hp. Twój exp: {experience}",
    "notimplemented": "Ta komenda jeszcze nie działa.",
}


# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    playsound("/home/socek/Downloads/war2/WarCraft 2 Sounds/Ships/Hshpwht3.wav")


async def chatgra(cmd: ChatCommand):
    print("chatgra")
    await cmd.send(TEXTS["intro"])


async def postac(cmd: ChatCommand):
    print("postac", cmd.text)
    profile = get_profile(ProfileIdentity(cmd.user.id, cmd.room.name))
    text = TEXTS["postać"].format(
        name=cmd.user.name,
        attack=profile.attack,
        defence=profile.defence,
        hp=profile.hp,
        experience=profile.experience,
    )
    print("a", text)
    print(await cmd.reply(text))


async def quest(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


async def walcz(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


async def topzywych(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


async def topall(cmd: ChatCommand):
    await cmd.send(TEXTS["notimplemented"])


def register(chat: Chat):
    chat.register_command("czatgra", chatgra)
    chat.register_command("postac", postac)
    chat.register_command("quest", quest)
    chat.register_command("walcz", walcz)
    chat.register_command("topzywych", topzywych)
    chat.register_command("topall", topall)
