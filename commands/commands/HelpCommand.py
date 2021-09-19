import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from utils.override import override
from commands.Command import WDCommand

@register_command
class HelpCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "help", ["h"])
    

@main_command("Just a pog command", HelpCommand)
async def on_command(message: Message, user: discord.Member, *,text: str):
    await message.reply(user.mention + ", Very pog message received: " + text)
