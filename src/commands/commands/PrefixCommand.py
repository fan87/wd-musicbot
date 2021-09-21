import inspect
import typing

import InstanceManager
import wdutils.MessageUtil
from Bot import WDMusicBot
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand


@register_command
class PrefixCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "prefix", ["cmdstart", "commandstart", "cmd-start", "command-start"])


@main_command("設定指令前綴", PrefixCommand, prefix = "前綴 | DEFAULT")
async def on_command(message: Message, prefix: str) -> None:
    bot = InstanceManager.mainInstance
    if prefix.upper() == "DEFAULT":
        bot.data.get_guild(typing.cast(discord.Guild, message.guild)).prefix = "__ DEFAULT __"
        bot.configsManager.save_data()
        await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 成功設置指令前綴回預設值: `" + bot.commandsManager.get_prefix(message.guild) + "`", discord.Colour.green(),
                                                      message)
        return

    bot.data.get_guild(typing.cast(discord.Guild, message.guild)).prefix = prefix
    bot.configsManager.save_data()

    await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 成功設置指令前綴至: `" + prefix + "`", discord.Colour.green(),
                                                  message)

