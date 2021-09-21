import asyncio
import concurrent
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from locale import Error
from typing import Any, Optional, Union, cast
import discord
import pykson
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
from events.EventManager import DiscordEventType
from youtube import YoutubeAPI

if TYPE_CHECKING:
    from Bot import WDMusicBot


class Track(pykson.JsonObject):
    name: str = pykson.StringField()
    author: str = pykson.StringField()
    video_id: str = pykson.StringField()
    length: int = pykson.IntegerField()  # Unit: Sec

    def __init__(self, name: str, author: str, video_id: str, length: int, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.author = author
        self.video_id = video_id
        self.length = length


class GuildPlayer:
    guild: Guild = None
    repeat_queue: bool = False



    _music_manager = None
    _bass: float = 0

    @property
    def bass(self) -> float:
        return self._bass

    @bass.setter
    def bass(self, value: float) -> None:
        self._bass = value
        try:
            self.get_audio_source().set_bass(value)
        except:
            pass


    @property
    def tracks(self) -> list[Track]:
        return self.get_music_manager().bot.data.get_guild(self.guild).queue

    @tracks.setter
    def tracks(self, queue: list[Track]) -> None:
        self.get_music_manager().bot.data.get_guild(self.guild).queue = queue
        self.get_music_manager().bot.configsManager.save_data()

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

    def append(self, track: Track) -> None:
        self.tracks.append(track)
        self.get_music_manager().bot.configsManager.save_data()

    def pop(self, index: int) -> Track:
        track = self.tracks.pop(index)
        self.get_music_manager().bot.configsManager.save_data()
        return track

    def clear(self) -> None:
        self.tracks.clear()
        self.get_music_manager().bot.configsManager.save_data()

    def next(self) -> Union[None, Track]:
        old_track: Track = self.pop(0)
        if self.repeat_queue:
            self.append(old_track)

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

    def remove(self, index: int) -> Union[Track, None]:
        try:
            track = self.tracks[index]
            if index == 0:
                tmp = self.repeat_queue
                self.repeat_queue = False
                self.skip()
                self.repeat_queue = tmp
                return track
            self.pop(index)
            return track
        except:
            return None

    def __init__(self, guild: Guild, music_manager: 'MusicManager') -> None:
        self.guild = guild
        self._music_manager = music_manager

    def get_voice_client(self) -> VoiceClient:
        return self.guild.voice_client

    def __play_song(self, video_id: str) -> None:
        import InstanceManager
        try:
            dir_url = youtube.YoutubeAPI.sync_get_dir_url(251, video_id)
            self.get_voice_client().play(music.WDAudioSource.WDVolumeTransformer(
                music.WDAudioSource.WDFFmpegPCMAudio(dir_url,
                                                     before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                                     options='-vn'
                                                     ),
                volume=self.get_music_manager().bot.data.get_guild(self.guild).volume),
                after=self.__after)
            self.get_audio_source().set_bass(self.bass)
        except Error as er:
            print(er)

    def play_track(self, track: Track) -> None:
        self.__play_song(track.video_id)

    skipped: bool = False

    def __after(self, error: Error) -> None:
        if not self.skipped:
            try:
                self.skip()
            except:
                pass

    async def add_to_queue(self, track: Track) -> bool:
        if self.get_current_track() is None:
            self.append(track)
            self.play_track(track)
            return True
        else:
            self.append(track)
            return False

    def fast_add_youtube_to_queue(self, youtube: YouTube) -> Track:

        def inner() -> Track:
            details = YoutubeAPI.sync_get_video_details(youtube.video_id)
            return Track(name=details["title"], author="author", video_id=youtube.video_id, length=int(details["lengthSeconds"]))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(inner)
            track = future.result()
            if self.get_current_track() is None:
                self.append(track)
                print("Added Song")
                self.play_track(track)
                return track
            else:
                print("Added Song")
                self.append(track)
                return track



    def skip(self, amount: int = 1) -> bool:
        if self.get_voice_client() is None:
            self.clear()
            return False
        if self.get_voice_client().is_playing():
            self.skipped = True
            self.get_voice_client().stop()
            self.skipped = False
        next_track: Union[Track, None] = None
        for i in range(amount):
            next_track = self.next()
        if next_track is None:
            return False
        else:

            self.play_track(cast(Track, next_track))

            return True

    async def get_track_from_youtube(self, youtube_url: str) -> Track:
        yt: YouTube = YouTube(youtube_url)
        return Track(yt.title, yt.author, str(yt.video_id), yt.length)

    async def get_track_from_youtube_pytube(self, yt: pytube.YouTube) -> Track:
        def get_title() -> str:
            return yt.title
        def get_author() -> str:
            return yt.author
        def get_length() -> int:
            return yt.length
        executor = ThreadPoolExecutor(max_workers=10)
        results = await asyncio.gather(
            asyncio.get_event_loop().run_in_executor(executor, get_title),
            asyncio.get_event_loop().run_in_executor(executor, get_author),
            asyncio.get_event_loop().run_in_executor(executor, get_length),
        )
        executor.shutdown()

        return Track(results[0], results[1], str(yt.video_id), results[2])


class MusicManager:
    bot: 'WDMusicBot' = None
    players: list = []

    def __init__(self, bot: 'WDMusicBot') -> None:
        self.bot = bot
        bot.eventManager.add_listener(DiscordEventType.ON_READY, self.ready)

    async def ready(self) -> None:
        bot = self.bot
        bot.ready = True
        for guild in bot.data.guilds:
            if guild.last_vc != 0:
                try:
                    dcguild: Guild = bot.get_guild(guild.guild_id)
                    channel: discord.VoiceChannel = dcguild.get_channel(guild.last_vc)
                    await channel.connect()
                    guild_player: GuildPlayer = self.get_guild_player(dcguild)
                    if len(guild_player.tracks) >= 1:
                        guild_player.play_track(cast(Track, guild_player.get_current_track()))
                    else:
                        raise Error()
                except Error as err:
                    guild.last_vc = 0
                    bot.configsManager.save_data()

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
