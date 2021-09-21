import asyncio
import typing

import InstanceManager
import wdutils.MessageUtil
from Bot import WDMusicBot
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from wdutils.override import override
from commands.Command import WDCommand


@register_command
class QueueCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "queue", ["q"], "資訊類")



async def on_command(message: Message) -> None:
    import InstanceManager
    bot: WDMusicBot = InstanceManager.mainInstance
    if len(bot.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).tracks) == 0:
        await wdutils.MessageUtil.reply_fancy_message("目前並沒有任何待播歌曲", discord.Colour.red(), message)
        return
    msg: str = "> **歌曲清單**\n```"
    index: int = 0
    for track in bot.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).tracks:
        msg += str(index) + ". " + track.name + "   (由 " + track.author + " 製作)\n"
        index += 1
    msg += "```"
    await message.reply(msg, mention_author=False)


@main_command("顯示所有以被排序的歌曲清單", QueueCommand, page="頁數")
async def playlist_contents(message: Message, page: int = 1) -> None:
    guild_player = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
    embed: discord.Embed = discord.Embed()
    if int(len(guild_player.tracks) / 5.0) + 1 < page:
        page = int(len(guild_player.tracks) / 5.0) + 1
    embed.title = "待播清單的內容 (頁數: " + str(page) + "/" + str(int(len(guild_player.tracks) / 5.0) + 1) + ")"
    i: int = 5 * (page - 1)
    start: bool = False
    ii: int = i
    for track in guild_player.tracks[i:i + 5]:
        if not start:
            embed.description = "```\n"
            start = True
        ii += 1
        embed.description += str(ii - 1) + ". " + track.name + "   (由 " + track.author + " 製作)\n"
    if start:
        embed.description += "```"
    if len(guild_player.tracks) == 0:
        embed.description = f"看似目前還沒有任何影片! 使用{InstanceManager.mainInstance.commandsManager.get_prefix(message.guild)}play 看看吧!"
    embed.colour = discord.Colour.blue()
    await message.reply(f"> {embed.title}\n{embed.description}", mention_author=False)