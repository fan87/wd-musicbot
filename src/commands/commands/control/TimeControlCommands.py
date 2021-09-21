import asyncio
from asyncio.events import AbstractEventLoop

import typing

import InstanceManager
import utils.MessageUtil
from music.MusicManager import GuildPlayer
from utils import MessageUtil, TimeParser
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand


@register_command
class ForwardCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "fast-forward", ["jump-forward", "jf", "ff", "fastforward", "forward"],
                         category="控制類")


@main_command(description="快轉", head_command=ForwardCommand, seconds="秒數")
async def forward_main(message: Message, seconds: float) -> None:
    guild_player: GuildPlayer = InstanceManager.mainInstance.musicManager.get_guild_player(
        typing.cast(discord.Guild, message.guild))
    if guild_player.get_voice_client() is None:
        await MessageUtil.reply_fancy_message(
            ":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(
                message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if guild_player.get_current_track() is None:
        await MessageUtil.reply_fancy_message(
            ":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(
                message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return

    guild_player.get_audio_source().jump(min(max(int(guild_player.get_audio_source().time/1000) + int(seconds), 0),
                                             guild_player.get_current_track().length) * 1000)
    await utils.MessageUtil.reply_fancy_message(":fast_forward: 成功快轉 " + seconds.__str__() + " 秒",
                                                discord.Colour.green(), message)


@register_command
class RewindCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "rewind",
                         ["jump-backward", "fb", "fr", "r", "fast-rewind", "fastrewind", "backward", "fast-backward",
                          "fastbackward"], category="控制類")


@main_command(description="倒帶", head_command=RewindCommand, seconds="秒數")
async def rewind_main(message: Message, seconds: float) -> None:
    guild_player: GuildPlayer = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
    if guild_player.get_voice_client() is None:
        await MessageUtil.reply_fancy_message(
            ":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(
                message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if guild_player.get_current_track() is None:
        await MessageUtil.reply_fancy_message(
            ":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(
                message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return

    guild_player.get_audio_source().jump(min(max(int(guild_player.get_audio_source().time/1000) - int(seconds), 0),
                                             guild_player.get_current_track().length) * 1000)
    await utils.MessageUtil.reply_fancy_message(":rewind: 成功倒帶 " + seconds.__str__() + " 秒",
                                                discord.Colour.green(), message)


@register_command
class SeekCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "seek",
                         ["jump-to", "jt", "jumpto"], category="控制類")


@main_command(description="跳到目標秒數", head_command=SeekCommand, seconds="秒數")
async def seek_main(message: Message, seconds: float) -> None:
    guild_player: GuildPlayer = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
    if guild_player.get_voice_client() is None:
        await MessageUtil.reply_fancy_message(
            ":x: 機器人尚未加入語音頻道! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(
                message.guild) + "join 讓機器人加入語音頻道", discord.Colour.red(), message)
        return
    if guild_player.get_current_track() is None:
        await MessageUtil.reply_fancy_message(
            ":x: 機器人並未播放任何歌曲! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(
                message.guild) + "play 讓機器人開始播放音樂", discord.Colour.red(), message)
        return

    guild_player.get_audio_source().jump(
        min(max(int(seconds), 0), guild_player.get_current_track().length) * 1000)
    await utils.MessageUtil.reply_fancy_message(":arrow_right: 成功跳至 " + TimeParser.parse(int(seconds)) + "",
                                                discord.Colour.green(), message)
