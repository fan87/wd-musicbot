from types import coroutine
import discord
from discord.message import Message
import inspect
from commands.CommandsManager import CommandsManager, main_command


class WDCommand:

    name: str = ""
    alias: list = []
    commandsManager: CommandsManager = None

    def __init__(self, commandsManager: CommandsManager, name: str, aliases: list) -> None:
        self.commandsManager = commandsManager
        self.name = name
        self.alias = aliases

    def __call__(self, message: Message):
        pass

