import asyncio
from asyncio.events import AbstractEventLoop
from utils import MessageUtil
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand

@register_command
class JoinCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "join", ["j"])

@main_command(description="Join user's channel", head_command=JoinCommand)
async def join(message: Message) -> None:
    if message.author.voice is None:
        return await MessageUtil.reply_fancy_message("請先加入一個語音頻道", discord.Colour.red(), message)

    if message.guild.voice_client is not None:
        return await MessageUtil.reply_fancy_message("機器人早已在其他頻道", discord.Colour.red(), message)


    loop: AbstractEventLoop = asyncio.get_event_loop()
    loop.create_task(message.author.voice.channel.connect())
    return await MessageUtil.reply_fancy_message("成功加入語音頻道", discord.Colour.green(), message)
