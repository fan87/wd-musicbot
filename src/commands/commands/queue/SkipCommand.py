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
class SkipCommand(commands.Command.WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "skip", [], "待播清單控制類")

@main_command("跳過歌曲", SkipCommand, amount="歌曲數量")
async def on_command(message: Message, amount: int = 1) -> None:
    if InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).get_voice_client() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).get_current_track() is None:
        await MessageUtil.reply_fancy_message(":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return
    count: int = 0
    for i in range(amount):
        if InstanceManager.mainInstance.musicManager.get_guild_player(typing.cast(discord.Guild, message.guild)).skip():
            count += 1
        else:
            break

    await utils.MessageUtil.reply_fancy_message(":white_check_mark: 成功跳過 " + str(count) + " 首歌曲", discord.Colour.green(), message)
