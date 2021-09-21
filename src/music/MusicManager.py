import asyncio
import random
import threading
from locale import Error
from typing import Any, Optional, Union, cast
import discord
import pytube
import typing
from discord import voice_client, Message
from discord.guild import Guild
from discord.player import PCMVolumeTransformer
from discord.voice_client import VoiceClient
from pytube.__main__ import YouTube
from pytube.streams import Stream

from typing import TYPE_CHECKING

import music.WDAudioSource
import youtube.YoutubeAPI

if TYPE_CHECKING:
    from Bot import WDMusicBot


class Track:
    name: str = ""
    author: str = ""
    video_id: str = ""
    length: int = 0  # Unit: Sec

    def __init__(self, name: str, author: str, video_id: str, length: int) -> None:
        self.name = name
        self.author = author
        self.video_id = video_id
        self.length = length


class GuildPlayer:
    guild: Guild = None
    tracks: 'list[Track]' = []
    repeat_queue: bool = False

    _music_manager = None

    def get_audio_source(self) -> music.WDAudioSource.WDVolumeTransformer:
        return self.get_voice_client().source

    def get_music_manager(self) -> 'MusicManager':
        return cast('MusicManager', self._music_manager)

    def get_current_track(self) -> Union[None, Track]:
        if len(self.tracks) >= 1:
            return self.tracks[0]
        else:
            return None

    def has_next(self) -> bool:
        return len(self.tracks) >= 2

    def next(self) -> Union[None, Track]:
        old_track: Track = self.tracks.pop(0)
        if self.repeat_queue:
            self.tracks.append(old_track)

        if len(self.tracks) >= 1:
            return self.tracks[0]
        else:
            return None

    def shuffle(self) -> None:
        if len(self.tracks) <= 1:
            pass
        shuffle = []
        for track in self.tracks:
            shuffle.append(track)
        shuffle.pop(0)
        random.shuffle(shuffle)
        new_tracks = [self.tracks[0]]
        for track in shuffle:
            new_tracks.append(track)
        self.tracks = new_tracks
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
        self._music_manager = music_manager

    def get_voice_client(self) -> VoiceClient:
        return self.guild.voice_client

    async def __play_song(self, video_id: str) -> None:
        import InstanceManager
        dir_url = await youtube.YoutubeAPI.get_dir_url(251, video_id)
        self.get_voice_client().play(music.WDAudioSource.WDVolumeTransformer(
            music.WDAudioSource.WDFFmpegPCMAudio(dir_url,
                                                 before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                                 options='-vn'
                                                 ),
            volume=self.get_music_manager().bot.data.get_guild(self.guild).volume),
            after=self.__after)

    async def __play_track(self, track: Track) -> None:
        await self.__play_song(track.video_id)

    skipped: bool = False

    def __after(self, error: Error) -> None:
        if not self.skipped:
            self.skip()


    async def add_to_queue(self, track: Track) -> bool:
        if self.get_current_track() is None:
            self.tracks.append(track)
            await self.__play_track(track)
            return True
        else:
            self.tracks.append(track)
            return False

    def skip(self) -> bool:
        if self.get_voice_client() is None:
            self.tracks.clear()
        if self.get_voice_client().is_playing():
            self.skipped = True
            self.get_voice_client().stop()

        next_track: Union[Track, None] = self.next()
        if next_track is None:
            return False
        else:

            def play_track() -> None:
                loop = asyncio.new_event_loop()
                future = loop.create_task(self.__play_track(cast(Track, next_track)))
                loop.run_until_complete(future)
                loop.close()

            thread: threading.Thread = threading.Thread(target=play_track)
            thread.start()

            return True

    async def get_track_from_youtube(self, youtube_url: str) -> Track:
        yt: YouTube = YouTube(youtube_url)
        return Track(yt.title, yt.author, str(yt.video_id), yt.length)

    async def get_track_from_youtube_pytube(self, yt: pytube.YouTube) -> Track:
        return Track(yt.title, yt.author, str(yt.video_id), yt.length)


class MusicManager:
    bot: 'WDMusicBot' = None
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

    def get_guild_player_by_message(self, message: Message) -> GuildPlayer:
        guild: Guild = cast(Guild, message.guild)
        for player in self.players:
            guild_player: GuildPlayer = player
            if guild.id == guild_player.guild.id:
                return player
        player: GuildPlayer = GuildPlayer(guild, self)
        self.players.append(player)
        return player
