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
class RemoveCommand(commands.Command.WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "remove", ["del"], "待播清單控制類")

@main_command("從待播歌單移除歌曲", RemoveCommand, index="歌曲ID")
async def remove_command(message: Message, index: int) -> None:
    guild_player: GuildPlayer = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
    if guild_player.get_voice_client() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if guild_player.get_current_track() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return

    length: int = len(guild_player.tracks)
    guild_player.remove(index)
    await wdutils.MessageUtil.reply_fancy_message(f":white_check_mark: 成功移除 1 首歌曲", discord.Colour.green(), message)
