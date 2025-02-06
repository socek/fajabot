from twitchAPI.chat import Chat
from twitchAPI.chat import EventData
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import ChatEvent

from fajabot import settings
from fajabot.commands import register


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print("Bot is ready for work, joining channels")
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(settings.TARGET_CHANNEL)
    # you can do other bot initialization things in here


# this is where we set up the bot
async def ttvloop():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(settings.APP_ID, settings.APP_SECRET)
    auth = UserAuthenticator(twitch, settings.USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, settings.USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want
    register(chat)

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)

    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input("press ENTER to stop\n")
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()
