import typing

import discord
from discord import Message

import InstanceManager
import commands.Command
import wdutils.MessageUtil
from Bot import WDMusicBot
from commands.CommandsManager import CommandsManager, register_command, main_command
from wdutils import MessageUtil


@register_command
class RepeatCommand(commands.Command.WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "repeat", ["loop"], "待播清單控制類")

@main_command("重複播放清單", RepeatCommand)
async def on_command(message: Message) -> None:

    guild_player = InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild))
    if guild_player.repeat_queue:
        guild_player.repeat_queue = False
        await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 關閉: 重複播放清單", discord.Colour.green(), message)
    else:
        guild_player.repeat_queue = True
        await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 開啟: 重複播放清單", discord.Colour.green(), message)