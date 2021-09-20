import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand

@register_command
class JoinCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "join", ["j"])

@main_command(description="Join user's channel", head_command=JoinCommand)
async def join(message: Message):
    if message.author.voice is None:
        return await message.channel.send("**[Beta Version Music Bot]**你沒有在語音頻道")

    if message.guild.voice_client is not None:
        return await message.channel.send("**[Beta Version Music Bot]**已在語音頻道")

    await message.author.voice.channel.connect() #語音.頻道.加入()
    return await message.channel.send("**[Beta Version Music Bot]**加入語音頻道")