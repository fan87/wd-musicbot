from logging import Logger

from discord.flags import Intents
from commands.CommandsManager import CommandsManager
from dataSaver.ConfigsManager import ConfigsManager
from events.EventManager import DiscordEventManager, DiscordEventType

from typing import IO
import os

import discord
from pykson import Pykson

from dataSaver.BotConfig import BotConfig




Logger.level = "debug"



class WDMusicBot(discord.Client):
    
    eventManager: DiscordEventManager = None
    configsManager: ConfigsManager = None
    commandsManager: CommandsManager = None

    config: BotConfig = BotConfig()

    def __init__(self):
        
        super().__init__(intents=Intents.all())
        
        import InstanceManager
        InstanceManager.mainInstance = self

        self.eventManager = DiscordEventManager(self)
        self.configsManager = ConfigsManager(self)
        self.commandsManager = CommandsManager(self, self.config.prefix)
        

        self.commandsManager.init()

        
        print("機器人成功啟動，正在連線至Discord...")
        self.register_listeners()
        

    def register_listeners(self):
        self.eventManager.add_listener(DiscordEventType.ON_READY, self.ready_handling)

    def start_bot(self):
        self.run(self.config.token)

    async def ready_handling(self):
        print("機器人已經成功連線至Discord! ")



    

if __name__ == "__main__":
    print("成功啟動Python! 正在啟動機器人")
    bot = WDMusicBot()
    bot.start_bot()
