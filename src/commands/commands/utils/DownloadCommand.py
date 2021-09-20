import asyncio
import typing

import pytube

import utils.MessageUtil
import youtube.YoutubeAPI
from Bot import WDMusicBot
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from utils.override import override
from commands.Command import WDCommand


@register_command
class DownloadCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "download", ["dl"], "工具類")


@main_command("最快速度取得Youtube影片的音訊檔下載連結(只限WEBP格式且最高音質)", DownloadCommand, url="影片連結")
async def on_command(message: Message, url: str) -> None:
    try:
        video: pytube.YouTube = pytube.YouTube(url)
        dir_url: str = await youtube.YoutubeAPI.get_dir_url(251, video.video_id)
        await message.reply(dir_url + "\n檔案格式為Webm，並且用Opus編碼。Opus屬於有損編碼格式，但因為Youtube是使用Opus編碼影片的音訊，所以你最多得到有損的編碼格式。 \n若要轉成MP3請自行轉檔，本服務僅提供許多網站都沒有的直接從Youtube伺服器下載音訊檔案功能", mention_author=True)
    except:
        await utils.MessageUtil.reply_fancy_message(":x: 錯誤: 無法取得連結", discord.Colour.red(), message)
