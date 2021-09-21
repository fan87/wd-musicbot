import asyncio
import threading
from typing import ContextManager, cast

import re

import pytube

import utils.MessageUtil
import youtube.YoutubeAPI
from Bot import WDMusicBot
import discord

from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from music.MusicManager import GuildPlayer, MusicManager, Track
from utils import MessageUtil
from utils.override import override
from commands.Command import WDCommand

@register_command
class PlayCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "play", ["p", "search", "s"], category="控制類")
    

@main_command("播放一首歌", PlayCommand, song="影片連結")
async def on_command(message: Message, *, song: str) -> None:
    import InstanceManager


    guild_player: GuildPlayer = InstanceManager.mainInstance.musicManager.get_guild_player(
        cast(discord.Guild, message.guild))

    if song is None:
        await utils.MessageUtil.reply_fancy_message(":x: 請輸入要播放的`歌名/URL`", discord.Colour.red(), message)
        return
    if message.guild.voice_client is None:
        InstanceManager.mainInstance.data.get_guild(message.guild).last_vc = message.author.voice.channel.id
        InstanceManager.mainInstance.configsManager.save_data()
        await message.author.voice.channel.connect()
        await utils.MessageUtil.reply_fancy_message(":white_check_mark: 成功加入語音頻道", discord.Colour.green(), message)

    if message.author.voice.channel != guild_player.get_voice_client().channel:
        await MessageUtil.reply_fancy_message(":x: 機器人早已在其他頻道! 請使用" + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "leave", discord.Colour.red(), message)
        return


    try:
        yt: pytube.YouTube = pytube.YouTube(song)
    except:
        await utils.MessageUtil.reply_fancy_message(":mag: 搜尋中...", discord.Colour.gold(), message)
        result: youtube.YoutubeAPI.Search = await youtube.YoutubeAPI.search(song)

        if len(result.videos) <= 0:
            await utils.MessageUtil.reply_fancy_message(":grimacing: 抱歉我沒找到音樂，請再次使用指令搜尋", discord.Colour.red(), message)
            return
        yt = result.videos[0]
    track: Track = await guild_player.get_track_from_youtube_pytube(yt)
    if await guild_player.add_to_queue(track):
        embed: discord.Embed = discord.Embed()
        embed.title = yt.title
        embed.set_author(name=yt.author)
        embed.description = ":play_pause: 正在播放 " + "https://youtube.com/watch?v=" + yt.video_id
        embed.colour = discord.Colour.green()
        embed.set_image(url=f"https://i.ytimg.com/vi/{yt.video_id}/hq720.jpg")
        embed.url = f"https://www.youtube.com/watch?v={guild_player.get_current_track().video_id}"
        await message.reply(embed=embed, mention_author=False)
    else:
        embed = discord.Embed()
        embed.title = yt.title
        embed.set_author(name=yt.author)
        embed.description = ":white_check_mark: 已經排序 " + "https://youtube.com/watch?v=" + yt.video_id
        embed.colour = discord.Colour.green()
        embed.set_image(url=f"https://i.ytimg.com/vi/{yt.video_id}/hq720.jpg")
        embed.url = f"https://www.youtube.com/watch?v={guild_player.get_current_track().video_id}"
        await message.reply(embed=embed, mention_author=False)
