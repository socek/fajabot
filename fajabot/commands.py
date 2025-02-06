from playsound import playsound
from twitchAPI.chat import Chat
from twitchAPI.chat import ChatCommand


# this will be called whenever the !reply command is issued
async def test_command(cmd: ChatCommand):
    playsound("/home/socek/Downloads/war2/WarCraft 2 Sounds/Ships/Hshpwht3.wav")


async def chatgra(cmd: ChatCommand):
    print("Chat gra")


async def nowapostac(cmd: ChatCommand):
    print("Nowa postać")


async def walka(cmd: ChatCommand):
    print("Walka!")


async def topzywych(cmd: ChatCommand):
    print("Top zywych!")


async def topall(cmd: ChatCommand):
    print("Top all!")


def register(chat: Chat):
    chat.register_command("czatgra", chatgra)
    chat.register_command("nowapostac", nowapostac)
    chat.register_command("walka", walka)
    chat.register_command("topzywych", topzywych)
    chat.register_command("topall", topall)
