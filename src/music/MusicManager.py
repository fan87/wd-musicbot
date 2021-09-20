from locale import Error
import discord
from discord import voice_client
from discord.guild import Guild
from discord.player import PCMVolumeTransformer
from discord.voice_client import VoiceClient
from pytube.__main__ import YouTube
from pytube.streams import Stream


class GuildPlayer:
    
    guild: Guild = None
    music_manager = None
    

    def __init__(self, guild: Guild, music_manager) -> None:
        self.guild = guild
        self.music_manager = music_manager

    def get_voice_client(self) -> VoiceClient:
        return self.guild.voice_client

    def play_song(self, url: str):
        import InstanceManager
        stream: Stream =  YouTube(url).streams.get_by_itag(251)
        self.get_voice_client().play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(stream.url)), after=self.__after)
        pcmvolume: PCMVolumeTransformer = self.get_voice_client().source
        pcmvolume.volume = 0.2
    def __after(self, error: Error):
        print("After")


class MusicManager:

    bot = None
    players: list = []

    def __init__(self, bot) -> None:
        self.bot = bot
    
    def get_guild_player(self, guild: Guild) -> GuildPlayer:
        for player in self.players:
            guild_player: GuildPlayer = player
            if guild.id == guild_player.guild.id:
                return player
        player: GuildPlayer = GuildPlayer(guild, self)
        self.players.append(player)
        return player

    
        
    
    
