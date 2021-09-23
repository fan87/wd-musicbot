import pykson


class BotConfig(pykson.JsonObject):
    token: str = pykson.StringField("token") # type: ignore
    prefix: str = pykson.StringField("prefix") # type: ignore
    owner: list[int] = pykson.ListField(int, "owner_ids") # type: ignore

