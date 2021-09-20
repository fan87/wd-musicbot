# 水滴音樂機器人
一個能夠完整取代Groovy和Rythm的 [自主架設式](https://en.wikipedia.org/wiki/Self-hosting_(web_services)) 機器人
<br>

## 功能
- 自訂性 - 本機器人開放原始碼，只要你會寫Python，即可更改任何你想要的東西
- 快速設置 - 本機器人支援Docker，這代表只要兩個指令就能夠輕鬆開啟機器人
- 網頁控制台 - 傳承Rythm的傳統，我們製作了網頁控制台，這代表您將能夠使用您的瀏覽器控制這台機器人
- 還有更多...
<br>
<br>
<br>

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
<br>
<br>
<br>

# README 仍在製作中