import asyncio

from fajabot.game import fight
from fajabot.profile import ProfileIdentity
from fajabot.ttv import ttvloop

# # lets run our setup
asyncio.run(ttvloop())

# profile_id = ProfileIdentity("Socek", "#chan")
# print(fight(profile_id))
