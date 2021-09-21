import json
import typing
from typing import IO

from dataSaver.BotConfig import BotConfig
import os
from pykson import Pykson
from dataSaver.BotData import MainData

if typing.TYPE_CHECKING:
    from Bot import WDMusicBot

class ConfigsManager:

    bot: 'WDMusicBot' = None

    def __init__(self, bot: 'WDMusicBot') -> None:
        self.bot = bot
        try:
            os.mkdir("run/")
        except:
            pass
        try:
            config_file: IO = open("run/config.json", "r")
            bot.config = Pykson().from_json(config_file.read(), BotConfig)
            config_file.close()
        except:
            print("========== 水滴機器人 ==========")
            bot.config.token = input("請輸入機器人Token: ")
            bot.config.prefix = input("請輸入機器人指令Prefix: ")
            print("成功設定完成水滴機器人! 您隨時可以至run/config.json更改設定檔")
            open("run/config.json", "w").write(Pykson().to_json(bot.config))

        try:
            data_file: IO = open("run/data.json", "r")
            bot.data = Pykson().from_json(data_file.read(), MainData)
            data_file.close()
        except:
            bot.data.guilds = []
            open("run/data.json", "w").write(json.dumps(json.loads(Pykson().to_json(self.bot.config)), indent=4, sort_keys=True))

    def save_data(self) -> 'MainData':
        open("run/data.json", "w").write(json.dumps(json.loads(Pykson().to_json(self.bot.data)), indent=4, sort_keys=True))
        print(json.dumps(json.loads(Pykson().to_json(self.bot.data)), indent=4, sort_keys=True))
        return self.bot.data
