import pykson


class BotConfig(pykson.JsonObject):
    token: str = pykson.StringField("token")
    prefix: str = pykson.StringField("prefix")

