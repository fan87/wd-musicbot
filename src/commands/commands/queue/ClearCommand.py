import typing

import discord
from discord import Message

import InstanceManager
import commands.Command
import wdutils.MessageUtil
from Bot import WDMusicBot
from commands.CommandsManager import CommandsManager, register_command, main_command
from music.MusicManager import GuildPlayer
from wdutils import MessageUtil


@register_command
class SkipCommand(commands.Command.WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "skip", ["next"], "待播清單控制類")

@main_command("跳過歌曲", SkipCommand, amount="歌曲數量")
async def on_command(message: Message, amount: int = 1) -> None:
    guild_player: GuildPlayer = InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild))
    if guild_player.get_voice_client() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if guild_player.get_current_track() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return

    length: int = len(guild_player.tracks)
    guild_player.clear()
    guild_player.get_voice_client().stop()
    await wdutils.MessageUtil.reply_fancy_message(f":white_check_mark: 成功清除 {str(length)} 首歌曲", discord.Colour.green(), message)
