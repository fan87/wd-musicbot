import asyncio
import threading
from typing import ContextManager, cast

import re

import pytube

import utils.MessageUtil
from Bot import WDMusicBot
import discord

from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from music.MusicManager import GuildPlayer, MusicManager, Track
from utils.override import override
from commands.Command import WDCommand

@register_command
class PlayCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "play", ["p"])
    

@main_command("Just a pog command", PlayCommand, url="Youtube Link")
async def on_command(message: Message, *, song: str) -> None:
    import InstanceManager

    guild_player: GuildPlayer = InstanceManager.mainInstance.musicManager.get_guild_player(cast(discord.Guild, message.guild))
    
    if song is None:
        await utils.MessageUtil.reply_fancy_message(":x:請輸入要播放的`歌名/URL`", discord.Colour.red(), message)
        return

    if message.guild.voice_client is None:
        await utils.MessageUtil.reply_fancy_message(":x:沒有在語音頻道", discord.Colour.red(), message)
        return
    try:
        await utils.MessageUtil.reply_fancy_message(":mag:取得影片資訊中...", discord.Colour.gold(), message)
        yt: pytube.YouTube = pytube.YouTube(song)
    except:
        await utils.MessageUtil.reply_fancy_message(":mag:搜尋中...", discord.Colour.gold(), message)
        search: pytube.Search = pytube.Search(song)

        if len(search.results) <= 0:
            await utils.MessageUtil.reply_fancy_message(":grimacing:抱歉我沒找到音樂，請再次使用指令搜尋", discord.Colour.red(), message)
            return
        yt = search.results[0]

    await utils.MessageUtil.reply_fancy_message(":play_pause:正在播放 " + "https://youtube.com/watch?v=" + yt.video_id, discord.Colour.red(), message)
    thread: threading.Thread = threading.Thread(target=guild_player.add_to_queue, args=[guild_player.get_track_from_youtube("https://youtube.com/watch?v=" + yt.video_id)])
    thread.start()
