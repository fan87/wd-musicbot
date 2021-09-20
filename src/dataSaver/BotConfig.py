from pykson import *


class BotConfig(JsonObject):
    token: str = StringField("token")
    prefix: str = StringField("prefix")

