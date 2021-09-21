import asyncio
from asyncio.events import AbstractEventLoop

import typing

import InstanceManager
from wdutils import MessageUtil
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand

@register_command
class LeaveCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "leave", ["l", "quit", "q", "disconnect", "dc"], category="控制類")

@main_command(description="退出機器人所在的語音頻道", head_command=LeaveCommand)
async def leave(message: Message) -> None:

    if message.guild.voice_client is None:
        await MessageUtil.reply_fancy_message(":x: 機器人早已退出! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return

    loop: AbstractEventLoop = asyncio.get_event_loop()
    loop.create_task(message.author.voice.channel.connect())
    await message.guild.voice_client.disconnect()
    guild_player = InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild))
    guild_player.clear()
    InstanceManager.mainInstance.data.get_guild(message.guild).last_vc = 0
    await MessageUtil.reply_fancy_message(":white_check_mark: 已經退出語音頻道了! 感謝您的使用 :partying_face: ", discord.Colour.green(), message)
    return
