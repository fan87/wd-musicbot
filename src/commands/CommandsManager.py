import asyncio
import functools
from asyncio import AbstractEventLoop
from typing import TYPE_CHECKING, Any, Callable
import typing

import discord.user
from discord.channel import TextChannel
from discord.member import Member
from discord.message import Message
from discord.user import User
from events.EventManager import DiscordEventType
from functools import partial
from logging import Logger
import os
import inspect

if TYPE_CHECKING:
    from Bot import WDMusicBot
    from commands.Command import WDCommand


class CommandsManager:
    bot = None

    commands: dict = {}
    prefix: str = ""

    def __init__(self, bot: 'WDMusicBot', prefix: str) -> None:
        self.bot = bot
        self.prefix = prefix

    def get_prefix(self, guild: typing.Union[discord.Guild, Any]) -> str:
        return self.prefix
        
    def init(self) -> None:
        from commands.Command import WDCommand
        from Bot import WDMusicBot
        contents = os.walk("src/commands/commands/")
        for content in contents:
            path = content[0].replace("src/", "")
            folders = content[1]
            files = content[2]
            for file in files:
                if file.endswith(".py"):
                    np: str = path
                    if not np.endswith("/"):
                        np += "/"
                    filepath = np + file.replace(".py", "")
                    import_name = filepath.replace("/", ".")
                    module = __import__(import_name)
        bot: WDMusicBot = self.bot
        bot.eventManager.add_listener(DiscordEventType.ON_MESSAGE, self.process_command)

    async def process_command(self, message: Message) -> None:
        from commands.Command import WDCommand
        user: User = message.author
        if user.bot:
            return
        content: str = message.content
        if not content.startswith(self.get_prefix(message.guild)):
            channel: TextChannel = message.channel
            return
        command_name: str = content.split(" ")[0]
        command_name = command_name[int(1):int(len(command_name))]
        command: WDCommand = self.find_command(command_name)

        if command is None:
            return

        
        await self.invoke(command, message)

    async def invoke(self, command: 'WDCommand', message: Message) -> None:
        old_arguments: list[str] = message.content.split(" ")[1:]
        arguments: list[str] = []
        for arg in old_arguments:
            if arg != "":
                arguments.append(arg)
        
        parameters: list = [message]
        func = self.commands[command]["main"]
        count: int = -2
        starstar: str = ""
        starstarpara: Any = None
        for parameter in inspect.signature(func).parameters.items():
            count = count + 1
            if count == -1:
                continue
            para: inspect.Parameter = parameter[1]
            if para.kind == para.POSITIONAL_OR_KEYWORD:
                try:
                    arguments[count]
                except:
                    if not para.default == para.empty:
                        parameters.append(para.default)
                    else:
                        parameters.append(None)
                    continue
                try:
                    type: str = str(para).replace(" ", "").split(":")[1]
                    parameters.append(self.convert(message, arguments[count], type))
                except:
                    parameters.append(arguments[count])
                
            if para.kind == para.KEYWORD_ONLY:
                starstar = para.name
                try:
                    arguments[count]
                except:
                    starstarpara = None
                    if not para.default == para.empty:
                        starstarpara = para.default
                    continue
                i: int = -1
                argument: str = ""
                for a in arguments:
                    i += 1
                    if i >= count:
                        argument += a + " "
                if not 1 == -1:
                    argument = argument[:-1]
                try:
                    type = str(para).replace(" ", "").split(":")[1]
                    starstarpara = self.convert(message, argument, type)
                except:
                    starstarpara = argument
                break

        if starstar != "":
            loop: AbstractEventLoop = asyncio.get_event_loop()
            loop.create_task(func(*parameters, **{starstar: starstarpara}))
        else:
            loop = asyncio.get_event_loop()
            loop.create_task(func(*parameters))


    def convert(self, message: Message, stringIn: str, typeIn: str) -> Any:
        import InstanceManager

        if typeIn == "str":
            return stringIn
        if typeIn == "int":
            return int(stringIn)
        if typeIn == "float":
            return float(stringIn)
        if typeIn == "bool":
            return bool(stringIn)

        if typeIn == "discord.user.User" or typeIn == "discord.User":
            if stringIn.startswith("<@!") and stringIn.endswith(">"):
                uid: str = stringIn[3:-1]
                member: Member = InstanceManager.mainInstance.get_user(int(uid))
                return member
            if stringIn.startswith("<@") and stringIn.endswith(">"):
                uid = stringIn[2:-1]
                member = InstanceManager.mainInstance.get_user(int(uid))
                return member

        if typeIn == "discord.member.Member" or typeIn == "discord.Member":
            if stringIn.startswith("<@!") and stringIn.endswith(">"):
                uid = stringIn[3:-1]
                member = message.guild.get_member(int(uid))
                return member
            if stringIn.startswith("<@") and stringIn.endswith(">"):
                uid = stringIn[2:-1]
                member = message.guild.get_member(int(uid))
                return member

        return None


    def find_command(self, command_name: str) -> typing.Union['WDCommand', None]:
        from commands.Command import WDCommand
        for command in self.commands.keys():
            cmd: WDCommand = command
            if cmd.name.lower() == command_name.lower():
                return command
            for alias in cmd.alias:
                if alias.lower() == command_name.lower():
                    return command
        return None


def main_command(description: str, head_command: Any, **kwargs: Any) -> Callable[[Any], Any]:
    from commands.Command import WDCommand
    import InstanceManager

    if issubclass(WDCommand, head_command):
        raise TypeError("Head Command must extends WDCommand")
    
    def inner(func: Any) -> Any:
        import InstanceManager
        if not inspect.isfunction(func):
            raise TypeError("Registered non-function command executable")
        found: bool = False
        for instance in InstanceManager.mainInstance.commandsManager.commands.keys():
            if type(instance) == head_command:
                InstanceManager.mainInstance.commandsManager.commands[instance].update({"main": func, "main_description": description, "argument_info": kwargs})
                found = True
        if not found:
            raise LookupError("The Head Command is not registered. Please decorate with @register_command and define the class before the function. Also make sure the class is declared in the same file where you declared the function")
        return func

    return inner


def register_command(clazz: Any) -> Any:
    from commands.Command import WDCommand
    import InstanceManager

    if not inspect.isclass(clazz):
        raise TypeError("Registered non-class command")
    if issubclass(WDCommand, clazz):
        raise TypeError("Registered non-WDCommand class")
    InstanceManager.mainInstance.commandsManager.commands[clazz(InstanceManager.mainInstance.commandsManager)] = {}
    return clazz
