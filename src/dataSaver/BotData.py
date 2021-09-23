import typing

import discord
import pykson
import random
import string

from music.MusicManager import Track


class PlayListData(pykson.JsonObject):
    name: str = pykson.StringField() # type: ignore
    share_id: str = pykson.StringField() # type: ignore
    tracks: list[Track] = pykson.ObjectListField(Track)

    def generate_share_id(self) -> str:
        import InstanceManager
        self.share_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=100))
        InstanceManager.mainInstance.configsManager.save_data()
        return self.share_id

def generate_id() -> str:
    share_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=100))
    return share_id

class GuildData(pykson.JsonObject):
    guild_id: int = pykson.IntegerField() # type: ignore
    volume: float = pykson.FloatField(default_value=float(1)) # type: ignore
    queue: list[Track] = pykson.ObjectListField(Track) # type: ignore
    last_vc: int = pykson.IntegerField(default_value=0) # type: ignore
    playlists: list[PlayListData] = pykson.ObjectListField(PlayListData) # type: ignore
    prefix: str = pykson.StringField(default_value="__ DEFAULT __") # type: ignore

    def get_playlist(self, name: str) -> PlayListData:
        import InstanceManager
        for playlist in self.playlists:
            if playlist.name == name:
                return playlist
        playlist = PlayListData()
        playlist.name = name
        playlist.generate_share_id()
        self.playlists.append(playlist)
        InstanceManager.mainInstance.configsManager.save_data()
        return playlist

    def has_playlist(self, name: str) -> bool:
        for playlist in self.playlists:
            if playlist.name == name:
                return True
        return False


class MainData(pykson.JsonObject):
    guilds: list[GuildData] = pykson.ObjectListField(GuildData)

    def get_guild(self, guild: typing.Union[typing.Any, discord.Guild]) -> GuildData:
        import InstanceManager
        for g in self.guilds:
            if g.guild_id == typing.cast(discord.Guild, guild).id:
                return g
        g = GuildData()
        g.guild_id = typing.cast(discord.Guild, guild).id
        self.guilds.append(g)
        InstanceManager.mainInstance.configsManager.save_data()
        return g
