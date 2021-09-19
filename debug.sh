#!/bin/bash
cd /
echo "========== 水滴音樂機器人 Docker Image =========="
echo "感謝您選擇水滴音樂機器人。你剛剛啟動了一個Docker Image"
echo "這代表您已經成功安裝水滴音樂機器人了，這包括Python3自動安裝, 以及一些所需的模組"
echo "接下來，Docker將會嘗試啟動機器人"
echo "您隨時可以透過Ctrl + C強制關閉機器人，並進入本容器(Docker Container)的Ubuntu Terminal"
echo "這代表關閉機器人您並不會立刻關閉本容器，也代表您將能在關閉機器人後使用Ubuntu修改檔案"
echo "如果您不熟悉Ubuntu Terminal，請搜尋\"使用Ubuntu Bash修改檔案\"的關鍵字"
echo "nano已經預先安裝，代表你可以使用nano編輯檔案"
echo "更多資訊將會在關閉機器人後顯示!"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo ""
echo ""
echo "正在啟動Python..."
cd /WDMusicBot
python3 Bot.py