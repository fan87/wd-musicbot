from discord.message import Message
from commands.CommandsManager import CommandsManager


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

