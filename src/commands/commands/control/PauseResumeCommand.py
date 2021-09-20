import asyncio
from asyncio.events import AbstractEventLoop

import typing

import InstanceManager
from utils import MessageUtil
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand

@register_command
class PauseCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "pause/resume", ["pause", "resume", "pa"], category="控制類")

@main_command(description="暫停正在播放的音樂", head_command=PauseCommand)
async def join(message: Message) -> None:
    if InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).get_voice_client() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).get_current_track() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return


    guild_player = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
    if not guild_player.get_voice_client().is_paused():
        guild_player.get_voice_client().pause()
        await MessageUtil.reply_fancy_message(":pause_button: 暫停", discord.Colour.green(), message)
    else:
        guild_player.get_voice_client().resume()
        await MessageUtil.reply_fancy_message(":arrow_forward: 繼續", discord.Colour.green(), message)
