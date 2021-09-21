import asyncio
from asyncio.events import AbstractEventLoop
from wdutils import MessageUtil
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand

@register_command
class JoinCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "join", ["j", "c", "connect"], category="控制類")

@main_command(description="加入發送訊息者的頻道", head_command=JoinCommand)
async def join(message: Message) -> None:
    import InstanceManager
    if message.author.voice is None:
        await MessageUtil.reply_fancy_message(":x: 請先加入一個語音頻道", discord.Colour.red(), message)
        return

    if message.guild.voice_client is not None:
        await MessageUtil.reply_fancy_message(":x: 機器人早已在其他頻道! 請使用" + InstanceManager.mainInstance.commandsManager.get_prefix(message.guild) + "leave", discord.Colour.red(), message)
        return
    InstanceManager.mainInstance.data.get_guild(message.guild).last_vc = message.author.voice.channel.id
    InstanceManager.mainInstance.configsManager.save_data()
    loop: AbstractEventLoop = asyncio.get_event_loop()
    loop.create_task(message.author.voice.channel.connect())

    await MessageUtil.reply_fancy_message(":white_check_mark: 成功加入語音頻道", discord.Colour.green(), message)
    return
