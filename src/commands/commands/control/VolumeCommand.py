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
class VolumeCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "volume", ["v", "loud", "vol"], category="控制類")

@main_command(description="更改音量大小", head_command=VolumeCommand, volume="音量(1-100)")
async def join(message: Message, volume: int) -> None:

    guild_player = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
    vol: int = min(max(0, volume), 100)
    try:
        transformer: discord.PCMVolumeTransformer = guild_player.get_voice_client().source
        vol = min(max(0, volume), 100)
        transformer.volume = float(vol/100.0)
    except:
        pass
    emoji: str = ":loud_sound:"
    if vol <= 75:
        emoji = ":sound:"
    elif vol <= 25:
        emoji = ":speaker:"
    if vol == 0:
        emoji = ":mute:"
    guild_player.music_manager.bot.data.get_guild(message.guild).volume = float(vol/100.0)
    guild_player.music_manager.bot.configsManager.save_data()
    await MessageUtil.reply_fancy_message(emoji + " 調整音量至 " + str(vol) + "%", discord.Colour.green(), message)

