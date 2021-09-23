from discord.message import Message
from commands.CommandsManager import CommandsManager


class WDCommand:

    name: str = ""
    category: str = ""
    alias: list[str] = []
    commandsManager: CommandsManager
    usage: str = ""

    def __init__(self, commandsManager: CommandsManager, name: str, aliases: list[str], category: str = "", *, custom_usage: str = "") -> None:
        self.commandsManager = commandsManager
        self.name = name
        self.alias = aliases
        self.category = category
        self.usage = custom_usage

    def __call__(self, message: Message) -> None:
        pass

