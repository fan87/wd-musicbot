from dataSaver.BotConfig import BotConfig
import os
from pykson import Pykson

class ConfigsManager:

    bot = None

    def __init__(self, bot) -> None:
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