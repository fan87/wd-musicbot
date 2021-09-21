from discord.flags import Intents

import dataSaver.BotData
from music.MusicManager import MusicManager
from commands.CommandsManager import CommandsManager
from dataSaver.ConfigsManager import ConfigsManager
from events.EventManager import DiscordEventManager, DiscordEventType

import discord

from dataSaver.BotConfig import BotConfig



class WDMusicBot(discord.Client):
    
    eventManager: DiscordEventManager = None
    configsManager: ConfigsManager = None
    commandsManager: CommandsManager = None
    musicManager: MusicManager = None
    ready: bool = False

    config: BotConfig = BotConfig()
    data: dataSaver.BotData.MainData = dataSaver.BotData.MainData()

    def __init__(self) -> None:
        
        super().__init__(intents=Intents.all())
        
        import InstanceManager
        InstanceManager.mainInstance = self

        self.eventManager = DiscordEventManager(self)
        self.configsManager = ConfigsManager(self)
        self.commandsManager = CommandsManager(self, self.config.prefix)
        self.musicManager = MusicManager(self)

        self.commandsManager.init()

        
        print("機器人成功啟動，正在連線至Discord...")
        self.register_listeners()
        

    def register_listeners(self) -> None:
        self.eventManager.add_listener(DiscordEventType.ON_CONNECT, self.ready_handling)

    def start_bot(self) -> None:
        self.run(self.config.token)

    async def ready_handling(self) -> None:
        print("機器人已經成功連線至Discord! ")



    

if __name__ == "__main__":
    print("成功啟動Python! 正在啟動機器人")
    bot = WDMusicBot()
    bot.start_bot()


