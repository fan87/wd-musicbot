import asyncio
import inspect
import typing

import InstanceManager
import wdutils.MessageUtil
from Bot import WDMusicBot
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from commands.Command import WDCommand


@register_command
class PrefixCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "debug", ["eval", "exec"])

t: list[typing.Any] = [None]


async def async_exec(code: str, *args: typing.Any) -> typing.Any:
    global t
    globals()["t"] = [None]
    c: str = ""
    for line in code.split("\n"):
        c += "    " + line + "\n"
    out: dict[typing.Any, typing.Any] = {"t": t}
    out.update(globals())
    exec(f'message="hi"\nasync def _async_exec():\n{c}\nt[0] = asyncio.ensure_future(_async_exec())', out, *args)
    task: asyncio.Task = out["t"][0]
    result = str(await task)
    return result


out: list[typing.Any] = [None, None]


@main_command("除錯用指令(僅限開發者)", PrefixCommand, cmd="指令")
async def on_command(message: Message, *, cmd: str) -> None:
    if typing.cast(typing.Any, message.author).id in InstanceManager.mainInstance.config.owner:
        try:
            globals().update({"bot": InstanceManager.mainInstance, "message": message})
            ex_locals: dict[str, typing.Any]= {"bot": InstanceManager.mainInstance, "message": message}
            in_locals = {"bot": InstanceManager.mainInstance, "message": message, "input": None}
            in_locals.update(globals())
            out = [None, None]
            await message.channel.send(str(await async_exec(cmd, ex_locals)))
        except Exception as err:
            await message.channel.send("Something went wrong: " + str(err))
    else:
        await wdutils.MessageUtil.reply_fancy_message(":x: 您不是開發者", discord.Colour.red(), message)
