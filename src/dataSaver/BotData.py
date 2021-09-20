from pykson import *


class GuildData(JsonObject):
    guild_id: int = IntegerField()

class MainData(JsonObject):
    guilds: GuildData = ObjectField(GuildData)

