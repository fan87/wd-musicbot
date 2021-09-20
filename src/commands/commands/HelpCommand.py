import inspect
import typing

from Bot import WDMusicBot
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from utils.override import override
from commands.Command import WDCommand


@register_command
class HelpCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "help", ["h"])


@main_command("顯示所有指令及其功能", HelpCommand)
async def on_command(message: Message) -> None:
    embed: discord.Embed = discord.Embed()
    embed.title = "指令清單"
    embed.set_footer(text="https://github.com/fan87/wd-musicbot",
                     icon_url="https://cdn.discordapp.com/attachments/869133787085287464/889501949148426320/github.png")
    import InstanceManager
    commands_manager: CommandsManager = InstanceManager.mainInstance.commandsManager
    commands: dict[str, list[WDCommand]] = {}
    for command in commands_manager.commands.keys():
        cmd: WDCommand = command
        try:
            old: list[WDCommand] = commands[cmd.category]
            old.append(cmd)
            commands[cmd.category] = old
        except:
            commands.update({cmd.category: [cmd]})

    for category in commands.keys():
        if category == "":
            info: str = "```"
            i: int = 0
            for command in commands[category]:
                i += 1
                if not i == 1:
                    info += "\n"
                info += get_command_info(command, message.guild)
            info += "```"
            embed.description = info
        else:
            info = "```"
            i = 0
            for command in commands[category]:
                i += 1
                if not i == 1:
                    info += "\n"
                info += get_command_info(command, message.guild)
            info += "```"
            embed.add_field(name=category, value=info, inline=False)
    embed.set_author(name="水滴音樂機器人 [by fan87 & YYJ]", icon_url="https://cdn.discordapp.com/attachments/869133787085287464/889510796781043742/unknown.png", url="https://github.com/fan87/wd-musicbot")
    embed.colour = discord.Colour.blue()
    await message.reply(embed=embed, mention_author=False)


def get_command_info(command: WDCommand, guild: typing.Any) -> str:
    import InstanceManager
    commands_manager: CommandsManager = InstanceManager.mainInstance.commandsManager
    info: dict = commands_manager.commands[command]
    out: str = commands_manager.get_prefix(guild) + command.name
    if not command.usage == "":
        out += " " + command.usage + "  -  " + info["main_description"]
        return out
    i: int = 0
    for argument in inspect.signature(info["main"]).parameters.items():
        i = i + 1
        if i == 1:
            continue
        out += " "
        parameter: inspect.Parameter = argument[1]
        s: str = ""
        if parameter.empty == parameter.default:
            out += "<"
        else:
            out += "["
        name: str = ""
        if parameter.name in info["argument_info"].keys():
            name = info["argument_info"][parameter.name]
        else:
            name = parameter.name
        if parameter.kind == parameter.KEYWORD_ONLY:
            out += name + "..."
        else:
            out += name
        if parameter.empty == parameter.default:
            out += ">"
        else:
            out += "]"
    out += "  -  " + info["main_description"]
    return out