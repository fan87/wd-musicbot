import random
from locale import Error
from typing import Any, Optional, Union, cast
import discord
import pytube
import typing
from discord import voice_client
from discord.guild import Guild
from discord.player import PCMVolumeTransformer
from discord.voice_client import VoiceClient
from pytube.__main__ import YouTube
from pytube.streams import Stream

from typing import TYPE_CHECKING

import youtube.YoutubeAPI

if TYPE_CHECKING:
    from Bot import WDMusicBot


class Track:
    name: str = ""
    author: str = ""
    url: str = ""
    length: int = 0  # Unit: Sec

    def __init__(self, name: str, author: str, url: str, length: int) -> None:
        self.name = name
        self.author = author
        self.url = url
        self.length = length


class GuildPlayer:
    guild: Guild = None
    tracks: 'list[Track]' = []
    repeat_queue: bool = False

    music_manager = None

    def get_current_track(self) -> Union[None, Track]:
        if len(self.tracks) >= 1:
            return self.tracks[0]
        else:
            return None

    def has_next(self) -> bool:
        return len(self.tracks) >= 2

    def next(self) -> Union[None, Track]:
        if self.repeat_queue:
            self.tracks.append(self.tracks.pop(0))

        if len(self.tracks) >= 1:
            return self.tracks[0]
        else:
            return None

    def shuffle(self) -> None:
        random.shuffle(self.tracks)
        return None

    def __remove(self, index: int) -> Union[Track, None]:
        try:
            track = self.tracks[index]
            if index == 0:
                self.skip()
                return track
            self.tracks.pop(index)
            return track
        except:
            return None

    def __init__(self, guild: Guild, music_manager: 'MusicManager') -> None:
        self.guild = guild
        self.music_manager = music_manager

    def get_voice_client(self) -> VoiceClient:
        return self.guild.voice_client

    def __play_song(self, url: str) -> None:
        import InstanceManager
        self.get_voice_client().play(discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(url,
                                   before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                   options='-vn'
                                   )), after=self.__after)

    def __play_track(self, track: Track) -> None:
        self.__play_song(track.url)

    skipped: bool = False

    def __after(self, error: Error) -> None:
        if not self.skipped:
            print("After")
            if self.get_current_track() is None:
                return

            self.tracks.pop(0)
            if self.get_current_track() is not None:
                track: Optional[Track] = self.get_current_track()
                self.get_voice_client().stop()
                self.__play_track(cast(Track, track))
            return

    def add_to_queue(self, track: Track) -> bool:
        if self.get_current_track() is None:
            self.tracks.append(track)
            self.__play_track(track)
            return True
        else:
            self.tracks.append(track)
            return False

    def skip(self) -> bool:
        if self.get_current_track() is None:
            return False

        self.tracks.pop(0)
        if self.get_current_track() is not None:
            track: Optional[Track] = self.get_current_track()
            self.skipped = True
            self.get_voice_client().stop()
            self.__play_track(cast(Track, track))
        return True

    async def get_track_from_youtube(self, youtube_url: str) -> Track:
        yt: YouTube = YouTube(youtube_url)
        url = await youtube.YoutubeAPI.get_dir_url(251, yt.video_id)
        return Track(yt.title, yt.author, str(url), yt.length)


    async def get_track_from_youtube_pytube(self, yt: pytube.YouTube) -> Track:
        url = await youtube.YoutubeAPI.get_dir_url(251, yt.video_id)
        return Track(yt.title, yt.author, str(url), yt.length)



class MusicManager:
    bot = None
    players: list = []

    def __init__(self, bot: 'WDMusicBot') -> None:
        self.bot = bot

    def get_guild_player(self, guild: Guild) -> GuildPlayer:
        for player in self.players:
            guild_player: GuildPlayer = player
            if guild.id == guild_player.guild.id:
                return player
        player: GuildPlayer = GuildPlayer(guild, self)
        self.players.append(player)
        return player

