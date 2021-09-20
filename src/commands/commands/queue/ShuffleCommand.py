import typing

import discord
from discord import Message

import InstanceManager
import commands.Command
import utils.MessageUtil
from Bot import WDMusicBot
from commands.CommandsManager import CommandsManager, register_command, main_command
from utils import MessageUtil


@register_command
class ShuffleCommand(commands.Command.WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "shuffle", ["random", "shuf", "shu", "sh"], "待播清單控制類")

@main_command("打亂待播清單的所有歌曲", ShuffleCommand)
async def on_command(message: Message) -> None:
    if InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).get_voice_client() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).get_current_track() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return
    guild_player = InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild))
    if len(guild_player.tracks) == 1:
        await utils.MessageUtil.reply_fancy_message(":x: 待播清單只有一首歌，因此無法打亂", discord.Colour.red(), message)
        return
    guild_player.shuffle()
    await utils.MessageUtil.reply_fancy_message(":twisted_rightwards_arrows: 成功打亂 " + str(len(guild_player.tracks)) + " 首歌曲", discord.Colour.green(), message)
