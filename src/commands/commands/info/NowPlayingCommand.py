import asyncio
import threading
import typing
from music.MusicManager import Track

import music.WDAudioSource
import wdutils.MessageUtil
from Bot import WDMusicBot
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from wdutils import MessageUtil, TimeParser
from wdutils.override import override
from commands.Command import WDCommand


@register_command
class NowPlayingCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "nowplaying", ["song", "np", "now-playing", "current-song", "currentsong", "cs"], "資訊類")


@main_command("顯示所有以被排序的歌曲清單", NowPlayingCommand)
async def on_command(message: Message) -> None:
    import InstanceManager
    bot: WDMusicBot = InstanceManager.mainInstance
    guild_player = bot.musicManager.get_guild_player_by_message(message)
    if guild_player.get_voice_client() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if guild_player.get_current_track() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return
    embed: discord.Embed = discord.Embed()
    embed.set_author(name="ɴᴏᴡ ᴘʟᴀʏɪɴɢ: " + guild_player.get_current_track().name)
    embed.description = ""
    pcm: music.WDAudioSource.WDVolumeTransformer = guild_player.get_voice_client().source
    player: discord.player.AudioPlayer = guild_player.get_voice_client()._player
    progress: float = float(pcm.time/(guild_player.get_current_track().length*1000))
    pre: int = round(progress*25)
    post: int = 24 - pre
    embed.description += "─" * pre
    embed.description += "◉"
    embed.description += "─" * post
    embed.description += "\n"

    embed.description += "◄◄⠀"
    if guild_player.get_voice_client().is_paused():
        embed.description += ":arrow_forward:"
    else:
        embed.description += ":pause_button:"
    embed.description += "⠀►►  "
    embed.description += TimeParser.parse(int(pcm.time/1000)) + " / " + TimeParser.parse(int(guild_player.get_current_track().length))

    embed.set_image(url=guild_player.get_current_track().thumbnail)
    embed.set_footer(text="by " + guild_player.get_current_track().author)
    embed.colour = discord.Colour.blue()
    embed.url = f"https://www.youtube.com/watch?v={typing.cast(Track, guild_player.get_current_track()).video_id}"
    await message.reply(embed=embed, mention_author=False)
