from Bot import WDMusicBot
import discord
from discord.message import Message
from commands.CommandsManager import CommandsManager, main_command, register_command
from utils.override import override
from commands.Command import WDCommand

@register_command
class PlayCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "play", ["p"])
    

@main_command("Just a pog command", PlayCommand, url="Youtube Link")
async def on_command(message: Message, url: str):
    import InstanceManager
    await message.reply("Playing " + url + "...")
    InstanceManager.mainInstance.musicManager.get_guild_player(message.guild).play_song(url)