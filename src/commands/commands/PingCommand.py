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
class PingCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "ping", ["latency", "delay"])


@main_command("查看延遲", PingCommand)
async def on_command(message: Message) -> None:
    bot = InstanceManager.mainInstance
    latency: float = bot.latency
    if latency >= 1:
        colour: discord.Colour = discord.Colour.dark_red()
    elif latency >= 0.7:
        colour = discord.Colour.red()
    elif latency >= 0.4:
        colour = discord.Colour.dark_gold()
    elif latency >= 0.2:
        colour = discord.Colour.gold()
    elif latency >= 0:
        colour = discord.Colour.green()

    embeds: list[discord.Embed] = []
    embeds.append(wdutils.MessageUtil.get_fancy_embed(":ping_pong: 目前延遲 (非語音): " + str(round(float(latency * 1000))) + "ms",
                                                  colour))
    guild_player = bot.musicManager.get_guild_player_by_message(message)
    if guild_player.get_voice_client() is None:
        embeds.append(wdutils.MessageUtil.get_fancy_embed(":bulb: 讓機器人加入語音以取得與語音伺服器的延遲", discord.Colour.green()))
    else:
        try:
            latency = guild_player.get_voice_client().latency
            if latency >= 1:
                colour = discord.Colour.dark_red()
            elif latency >= 0.7:
                colour = discord.Colour.red()
            elif latency >= 0.4:
                colour = discord.Colour.dark_gold()
            elif latency >= 0.2:
                colour = discord.Colour.gold()
            elif latency >= 0:
                colour = discord.Colour.green()
            embeds.append(
                wdutils.MessageUtil.get_fancy_embed(":ping_pong: 目前語音延遲: " + str(round(float(latency * 1000))) + "ms",
                                                          colour))
        except:
            embeds.append(
                wdutils.MessageUtil.get_fancy_embed(":ping_pong: 目前語音延遲: 未知。請晚點再回來看看",
                                                          discord.Colour.green()))

    await message.reply(embed=embeds[0], mention_author=False)
    await message.channel.send(embed=embeds[1])

