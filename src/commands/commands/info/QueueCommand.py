import asyncio
import typing

import utils.MessageUtil
from Bot import WDMusicBot
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from utils.override import override
from commands.Command import WDCommand


@register_command
class QueueCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "queue", ["q"], "資訊類")


@main_command("顯示所有以被排序的歌曲清單", QueueCommand)
async def on_command(message: Message) -> None:
    import InstanceManager
    bot: WDMusicBot = InstanceManager.mainInstance
    if len(bot.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).tracks) == 0:
        await utils.MessageUtil.reply_fancy_message("目前並沒有任何待播歌曲", discord.Colour.red(), message)
        return
    msg: str = "> **歌曲清單**\n```"
    for track in bot.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).tracks:
        msg += track.name + "   (由 " + track.author + " 製作)\n"
    msg += "```"
    await message.reply(msg, mention_author=False)
