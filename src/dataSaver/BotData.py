import discord
import pykson

from music.MusicManager import Track


class GuildData(pykson.JsonObject):
    guild_id: int = pykson.IntegerField()
    volume: float = pykson.FloatField(default_value=float(1))
    queue: list[Track] = pykson.ObjectListField(Track)
    last_vc: int = pykson.IntegerField(default_value=0)

class MainData(pykson.JsonObject):
    guilds: list[GuildData] = pykson.ObjectListField(GuildData)

    def get_guild(self, guild: discord.Guild) -> GuildData:
        for g in self.guilds:
            if g.guild_id == guild.id:
                return g
        g = GuildData()
        g.guild_id = guild.id
        self.guilds.append(g)
        return g
