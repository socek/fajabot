from asyncio import TaskGroup
from asyncio import ensure_future
from asyncio import new_event_loop
from asyncio import run
from asyncio import sleep
from signal import SIGINT
from signal import SIGTERM
from signal import SIGUSR1
from signal import signal

from twitchAPI.chat import Chat
from twitchAPI.chat import EventData
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import ChatEvent

from fajabot import settings
from fajabot.commands import register
from fajabot.consts import State


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print("Bot is ready for work, joining channels")
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(settings.TARGET_CHANNEL)
    # you can do other bot initialization things in here
    await ready_event.chat.send_message(settings.TARGET_CHANNEL, "Bot Aktywny, można grać.")


class Application:
    def __init__(self):
        self.state = State.BEFORE_START
        self.twitch = None
        self.chat = None

    async def refresh(self):
        print("Initializing...")
        self.state = State.RUNNING
        self.twitch = await Twitch(settings.APP_ID, settings.APP_SECRET)
        auth = UserAuthenticator(self.twitch, settings.USER_SCOPE)
        print("Authorizing...")
        token, refresh_token = await auth.authenticate(browser_name="Firefox")
        await self.twitch.set_user_authentication(token, settings.USER_SCOPE, refresh_token)
        self.chat = await Chat(self.twitch)
        # register the handlers for the events you want
        register(self.chat)

        # listen to when the bot is done starting up and ready to join channels
        self.chat.register_event(ChatEvent.READY, on_ready)
        # self.chat.register_event(ChatEvent.JOINED, on_joined)

        # we are done with our setup, lets start this bot up!
        print("Starting chat...")
        self.chat.start()
        print("Started...")

    async def close(self):
        self.chat.stop()
        await self.twitch.close()

    async def wait_until_end(self):
        while self.state == State.RUNNING:
            await sleep(1)

    async def main(self):
        while self.state != State.EXITING:
            await self.refresh()
            await self.wait_until_end()
            await self.close()


def init(app):
    def exit_application(*args, **kwargs):
        print("\rExiting...")
        app.state = State.EXITING

    def restart(*args, **kwargs):
        print("\rRestarting...")
        app.state = State.RESTART

    for signalCode in [SIGINT, SIGTERM]:
        signal(signalCode, exit_application)
    signal(SIGUSR1, restart)


def main():
    app = Application()
    init(app)
    eloop = new_event_loop()
    run(app.main())
