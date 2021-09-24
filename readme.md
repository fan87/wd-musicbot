# 水滴音樂機器人
一個能夠完整取代Groovy和Rythm的 [自主架設式](https://en.wikipedia.org/wiki/Self-hosting_(web_services)) 機器人
<br>

# 已經停止維護
本專案已經停止維護! 目前還沒有維護者，並且目前有許多問題仍然存在！<br>
強烈推薦不要使用，但

## 功能
- 自訂性 - 本機器人開放原始碼，只要你會寫Python，即可更改任何你想要的東西
- 快速設置 - 本機器人支援Docker，這代表只要兩個指令就能夠輕鬆開啟機器人
- 還有更多...
<br>
<br>
<br>

## 安裝教學: 直接執行
如果您的伺服器正在使用Ubuntu，或者您確定您所使用的作業系統支援Ubuntu Docker Image(這可能包括您電腦支援WSL 2)，請改用 安裝教學: Docker<br>
本安裝方式極不推薦，但是這邊還是公開一下，畢竟還有人的Windows跑不了Docker

### 第一步: 下載
 您必須安裝Git，Git的下載能在 [本連結](https://git-scm.com/) 找到<br>
 安裝完成後，您就可以使用以下指令
```shell
git clone https://github.com/fan87/wd-musicbot.git
```
### 第二步: 更新/安裝 Python
要執行此機器人，***您必須安裝Python 3.9***<br>
若您正在使用Ubuntu，可直接使用以下指令:
```shell
sudo apt install -y python3.9
```
若您正在使用Windows，您可能會需要到Python官方網站下載最新版本的Python，並且將舊版Python的路徑從PATH移除。也因為這些複雜的安裝方式，Docker極為推薦
### 第三步: 執行
```shell
cd wd-musicbot
python src/Bot.py
```
### 第四步: 設置
類似於 安裝教學: Docker 設置


## 安裝教學: Docker
使用Docker安裝是最安全且最快速的方法，前提是你有一個好網路。<br>
若想了解關於Docker的詳情，請自行搜尋 <br>


### 第一步: 下載
安裝完Docker後，您必須下載我們最新的Docker Image。要下載，請使用以下指令:
```shell
docker pull fan87/wd-musicbot:latest
```
檔案大小大約為200-250MB，雖然看起來很大，但是有230MB是只要下載一次就可以。<br>
其中大約180MB就是Python3, YoutubeDL以及其他更多Dependency，而還有大約50MB是Ubuntu<br>

### 第二步: 啟動
下載後，請使用以下指令啟動機器人:
```shell
docker -it --name <Container 名稱> fan87/wd-musicbot:latest
```
Container名稱如果不想輸入，可以將指令改成:
```shell
docker -it fan87/wd-musicbot:latest
```
<br>
其中`-it`代表:<br>

1. Interactive - 可以輸入文字<br>
2. TTY - pseudo-TTY(我不確定是什麼意思)<br>

### 第三步: 設置
您將需要輸入Discord機器人的Token和Prefix。機器人Token取得方式網路上都有，可以自行搜尋，Prefix就是指令前綴，例如: `!play`的前綴就是`!`<br><br><br>
![](https://cdn.discordapp.com/attachments/869133787085287464/889572582100185119/unknown.png)
<br>⬆️ 啟動時大概會長這樣

> 詳細說明請閱讀啟動容器後顯示的文字

### 第四步: 關閉
若機器人仍在開啟狀態，您必須按Ctrl + C來停止機器人<br>
停止後，您將會需要退出Docker Container。您當然可以直接關閉視窗，不過這會讓Ubuntu在背景運行<br>
請輸入`exit`來完全關閉。<br>

### 第五步: 再次啟動
要再次啟動，可以使用以下指令看到所有的容器
```shell
docker ps -a
```
![](https://cdn.discordapp.com/attachments/869133787085287464/889573696883286108/unknown.png)
<br>在這邊可以看到IMAGE一欄，找到`fan87/wd-musicbot:latest` 或者類似的東西<br>
輸入以下指令停止容器:
```shell
docker container stop <容器ID>
```
範例中的容器ID(CONTAINER ID)為`ac4547caa8bf`，因此需要輸入`docker container stop ac4547caa8bf`<br>
<br>
如果您是使用`exit`關閉容器的，那麼這個容器應該早已關閉了。<br>
這代表如果有報任何錯誤，可能不是你的錯(例如Container has already stopped)
<br><br>
接著輸入以下指令開啟容器:
```
docker container start -ai <容器ID>
```
這邊的範例，我需要用`docker container start -ai ac4547caa8bf`<br>
`-ai`代表Attach和Interactive:

1. Attach - 能夠看到輸出，並且能輸入(如果不加`a`就會在背景運行)
2. Interactive - 能夠輸入

不用重新設定，機器人就打開了

### 重點: 背景運行
直接關閉視窗就能夠讓Docker Container在背景運行，而如果今天是用start指令，則不加`a`
<br>例如:
```shell
docker container start -i <容器ID>
```


## 安裝教學: Docker 自行建制
一般使用者建議不要自行建制。如果你是開發者，並且想要幫助這個專案，那您將會需要自行建制
### 第一步: 下載Repository
```shell
git clone https://github.com/fan87/wd-musicbot && cd wd-musicbot
```
### 第二步: 修改 build-docker.sh
修改成
```shell
cp --force DockerFiles/GithubRelease ./Dockerfile
docker container rm -f $(docker ps -a -q)
docker build -t wdmusic .
docker run -it wdmusic:latest
```
> **如果您在開發目錄有了`run`資料夾，請將`DockerFiles/GithubRelease`改成`DockerFiles/Release`**

### 第三步: 執行
```shell
./build-docker.sh
```

### 第四步: 啟動
建制完成後，已經自動啟動了<br>
下一步，同`Docker安裝教學: 關閉`

## 開發教學: 執行
若今天您想要在Docker開發，您可能不會想要每次都輸入一次Token和Prefix<br>
### 第一步: 下載Repository
```shell
git clone https://github.com/fan87/wd-musicbot && cd wd-musicbot
```
### 第二步: 執行
```shell
./debug-docker.sh
```
第一次需要比較久的時間，第二次就能夠在不到1秒開啟Docker Container

<br>
<br>

## 如何開發
這邊推薦使用Visual Studio Code，或者您擁有PyCharms Professional(可透過購買/GitHub學生帳號取得)可以使用PyCharms<br>
這邊不使用 PyCharms Community 是因為本Repository包含TypeScript, HTML, CSS，而PyCharms Community(也就是免費版)並不支援TypeScript, 和CSS。<br>
同時Visual Studio Code在設定正確的情況下能夠比PyCharms還要有更好的自動完成及效能優化。
這裡給一套推薦Pylance(微軟所開發的Python自動完成系統)的設定:
```json
{
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.memory.keepLibraryAst": true,
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnknownArgumentType": "none",
        "reportUnknownLambdaType": "none",
        "reportUnknownMemberType": "none",
        "reportUnknownParameterType": "none",
        "reportUnknownVariableType": "none",
        "reportMissingTypeStubs": "none",
        "reportUnusedVariable": "none",
        "reportUnusedFunction": "none",
        "reportUnusedImport": "none",
        "reportUnnecessaryComparison": "none",
        "reportUntypedBaseClass": "none",
        "reportUntypedFunctionDecorator": "none",
        "reportUntypedClassDecorator": "none",
        "reportOptionalMemberAccess": "none",
        "reportImportCycles": "warning"
    },
}
```
使用這套設定會剛好滿足本Repository的Code Style<br>
> ***但這套設定並不適用於所有人。請自行設計出屬於自己的設定***


好，回歸正題，如何開始開發?

(既然您會想要開發，我就是以你了解許多相關知識的情況描述，例如: 我不會說怎麼取得Discord機器人Token，或者你將會需要Git之類的廢話)
### 第一步: Clone
若要協助開發，請先Fork。<br>
若要用於私人版，可以使用下列方式:
```sh
git clone https://github.com/fan87/wd-musicbot
```
若您在GitHub有自己的Fork，請將https://github.com/fan87/wd-musicbot取代成該Repository的連結

### 第二步: 安裝Python 3.9
非常重要。如果您是使用Ubuntu:
```sh
sudo apt install python3.9
```
如果您是使用Windows，您需要從官方網站安裝Python3.9<br>
如果您電腦已經有舊版Python，您可能會需要將舊版的Python路徑從path移除<br>
或者，您可以使用Python Virtual Environment

### 第三步: 開始開發
這邊使用VS Code介紹<br>
首先先打開VS Code:
```sh
cd wd-musicbot
code . # 這行將會直接開啟VS Code
```
接下來，必須安裝所有的Dependencies:
```sh
python3.9 -m pip install requirements.txt # 如果您是使用Windows，請改為pip install requirements.txt，或者python -m pip install requirements.txt
```
又會者您是使用Virtual Environment(VENV)，請將python3.9改成venv/bin/python3.9或者其他python 3.9的路徑
### 第四步: 執行
如果您使用VS Code，在左邊Run and Debug能直接執行。<br>
如果您是使用PyCharms，請在Run Configuration裡面的Interpreter Options增加`-B`<br>
`-B`的用途是不要輸出__pycache__(如果git add . 會新增這些檔案至Git，這可能不是你想要的，同時: 這些資料夾有時看起來很煩)<br>

## 授權
本專案正在使用[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)<br>
詳情請查看LICENSE檔案


![](https://cdn.discordapp.com/attachments/869133787085287464/890594956203413545/unknown.png)
