import discord

import InstanceManager
import wdutils.MessageUtil
from commands.Command import WDCommand
from commands.CommandsManager import CommandsManager
import asyncio
from asyncio.events import AbstractEventLoop

from music.MusicManager import GuildPlayer
from wdutils import MessageUtil
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand


@register_command
class BassCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "bass", [], "效果類")


@main_command("低音go brr", BassCommand, value="低音加成程度(0% - 200%, 預設100%)")
async def bass_command(message: discord.Message, value: int) -> None:
    if value is None:
        guild_player: GuildPlayer = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
        await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 低音加成程度: " + str((guild_player.bass+20)*5) + "%!",
                                                      discord.Colour.green(),
                                                      message)
    else:
        guild_player = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
        guild_player.bass = min(max((value * (40 / 200)) - 20, -20), 20)
        await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 成功設置低音加成程度至 " + str((guild_player.bass+20)*5) + "%!",
                                                      discord.Colour.green(),
                                                      message)
