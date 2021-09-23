import discord
import pytube
import typing
from discord.message import Message

import InstanceManager
import wdutils.MessageUtil
from youtube import YoutubeAPI
from commands.Command import WDCommand
from commands.CommandsManager import CommandsManager, main_command, register_command
from dataSaver.BotData import PlayListData
from music.MusicManager import Track, GuildPlayer


@register_command
class CreatePlaylistCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "create-playlist", ["cpl", "cp", "addpl"], "播放清單控制")


@main_command("創立一個播放清單", CreatePlaylistCommand, name="播放清單名稱")
async def create_playlist(message: Message, name: str) -> None:
    if not InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(name):
        playlist = InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name)
        embed = wdutils.MessageUtil.get_fancy_embed(":white_check_mark: 成功建立播放清單: " + name + " !",
                                                    color=discord.Colour.green())
        await message.reply(embed=embed, mention_author=False)
    else:
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 這個名字已經被用過了! ", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)


@register_command
class ListPlaylistsCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "list-playlists", ["lspl"], "播放清單控制")


@main_command("顯示所有播放清單", ListPlaylistsCommand)
async def list_playlists(message: Message) -> None:
    if len(InstanceManager.mainInstance.data.get_guild(message.guild).playlists) <= 0:
        await wdutils.MessageUtil.reply_fancy_message(
            ":x: 本伺服器並沒有任何播放清單! 請使用 " + InstanceManager.mainInstance.commandsManager.get_prefix(
                message.guild) + "create-playlist 來創建播放清單! ", discord.Colour.red(), message)
        return
    out: str = "```\n"
    for playlist in InstanceManager.mainInstance.data.get_guild(message.guild).playlists:
        out += playlist.name + "  (" + str(len(playlist.tracks)) + "部影片)\n"
    out += "```"
    await message.reply(out)


@register_command
class RemovePlaylistCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "remove-playlist", ["rmpl"], "播放清單控制")


@main_command("顯示所有播放清單", RemovePlaylistCommand, name="播放清單名稱")
async def remove_playlist(message: Message, name: str) -> None:
    if InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(name):
        playlist = InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name)
        InstanceManager.mainInstance.data.get_guild(message.guild).playlists.remove(playlist)
        InstanceManager.mainInstance.configsManager.save_data()
        embed = wdutils.MessageUtil.get_fancy_embed(":wastebasket: 成功刪除播放清單: " + name + " !",
                                                    color=discord.Colour.green())
        await message.reply(embed=embed, mention_author=False)
    else:
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 播放清單不存在!", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)


@register_command
class AddPlaylistCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "playlist-add", ["pladd"], "播放清單控制")


@main_command("在播放清單新增歌曲", AddPlaylistCommand, name="播放清單名稱", song="搜尋文字 | 連結")
async def add_playlist(message: Message, name: str, *, song: str) -> None:



    if InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(name):
        guild_player = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
        guild_playlist = InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name)
        count: int = 0

        try:
            playlist: pytube.Playlist = pytube.Playlist(song)
            playlist.videos
            playlist.title

            await wdutils.MessageUtil.reply_fancy_message("請稍後... 這可能須要一些時間。 ", discord.Colour.gold(), message)

            vid: typing.Any = None
            for video in playlist.videos:
                count = count + 1
                if count == 1:
                    vid = await guild_player.get_track_from_youtube_pytube(video)

                guild_playlist.tracks.append(await guild_player.get_track_from_youtube_pytube(video))
                InstanceManager.mainInstance.configsManager.save_data()

            embed = discord.Embed()
            embed.title = playlist.title
            embed.description = f":white_check_mark: 成功新增 {count} 部影片至播放清單"
            embed.colour = discord.Colour.green()
            embed.set_image(url=vid.thumbnail)
            embed.url = f"https://www.youtube.com/watch?v={vid.video_id}"
            await message.reply(embed=embed, mention_author=False)
            return
        except Exception as err:
            print(err)
            try:
                yt: pytube.YouTube = pytube.YouTube(song)
                yt.streams
            except:
                await wdutils.MessageUtil.reply_fancy_message(":mag: 搜尋中...", discord.Colour.gold(), message)
                result: YoutubeAPI.Search = await YoutubeAPI.search(song)

                if len(result.videos) <= 0:
                    await wdutils.MessageUtil.reply_fancy_message(":grimacing: 抱歉我沒找到音樂，請直接使用YouTube搜尋並輸入連結。值得注意的是: 直播目前不支援",
                                                                  discord.Colour.red(),
                                                                  message)
                    return
                yt = result.videos[0]

        track = await guild_player.get_track_from_youtube_pytube(yt)
        guild_playlist.tracks.append(track)
        InstanceManager.mainInstance.configsManager.save_data()
        embed = discord.Embed()
        embed.title = yt.title
        embed.set_author(name=yt.author)
        embed.description = ":white_check_mark: 成功新增 " + "https://youtube.com/watch?v=" + yt.video_id + " 至播放清單"
        embed.colour = discord.Colour.green()
        embed.set_image(url=yt.thumbnail_url)
        embed.url = f"https://www.youtube.com/watch?v={yt.video_id}"
        await message.reply(embed=embed, mention_author=False)
    else:
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 播放清單不存在!", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)
        return

@register_command
class RemovePlaylist(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "playlist-remove", ["plrm", "rm"], "播放清單控制")


@main_command("從播放清單移除歌曲。歌曲ID可使用 playlist-contents 指令取得", RemovePlaylist, name="播放清單名稱", index="歌曲ID")
async def playlist_remove(message: Message, name: str, index: int) -> None:

    if InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(name):
        if index <= len(InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name).tracks):
            track = InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name).tracks.pop(index-1)
            InstanceManager.mainInstance.configsManager.save_data()
            await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 成功從播放清單移除 `" + track.name + "`!",
                                                          discord.Colour.green(),
                                                          message)
        else:
            await wdutils.MessageUtil.reply_fancy_message(":x: 播放清單沒有那麼長! ",
                                                          discord.Colour.red(),
                                                          message)
    else:
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 播放清單不存在!", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)
        return


@register_command
class PlaylistInfoCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "playlist-info", ["info", "plinfo"], "播放清單控制")


@main_command("顯示播放清單詳細資料", PlaylistInfoCommand, name="播放清單名稱")
async def playlist_info(message: Message, name: str) -> None:
    if InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(name):
        playlist = InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name)
        embed: discord.Embed = discord.Embed()
        embed.title = name
        embed.add_field(name="清單大小", value=str(len(playlist.tracks)))
        embed.add_field(name="分享金鑰", value=f"`{playlist.share_id}`")
        embed.add_field(name="清單內容", value=f"`請使用{InstanceManager.mainInstance.commandsManager.get_prefix(message.guild)}playlist-contents <播放清單名稱>`")
        embed.colour = discord.Colour.blue()
        await message.reply(embed=embed, mention_author=False)

    else:
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 播放清單不存在!", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)


@register_command
class PlaylistContentsCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "playlist-contents", ["contents", "plctnt", "plls", "ls"], "播放清單控制")


@main_command("顯示播放清單內容", PlaylistContentsCommand, name="播放清單名稱", page="頁數")
async def playlist_contents(message: Message, name: str, page: int = 1) -> None:
    if InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(name):
        playlist = InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name)
        embed: discord.Embed = discord.Embed()
        pc = int(len(playlist.tracks)/5.0)
        if len(playlist.tracks) % 5.0 != 0:
            pc += 1
        if pc < page:
            page = pc
        embed.title = "`" + name + "` 的內容 (頁數: " + str(page) + "/" + str(pc) + ")"
        i: int = 5*(page - 1)
        start: bool = False
        ii: int = i
        for track in playlist.tracks[i:i+5]:
            if not start:
                embed.description = "```\n"
                start = True
            ii += 1
            embed.description += str(ii) + ". " + track.name + "   (由 " + track.author + " 製作)\n"
        if start:
            embed.description += "```"
        if len(playlist.tracks) == 0:
            embed.description = f"看似目前還沒有任何影片! 使用{InstanceManager.mainInstance.commandsManager.get_prefix(message.guild)}add-playlist 看看吧!"
        embed.colour = discord.Colour.blue()
        await message.reply(embed=embed, mention_author=False)

    else:
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 播放清單不存在!", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)


@register_command
class RenamePlaylist(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "rename-playlist", ["rmpl", "mvpl", "mv"], "控制類")


@main_command("重新命名播放清單", RenamePlaylist, name="播放清單名稱", new_name="新播放清單名稱")
async def rename_playlist(message: Message, name: str, new_name: str) -> None:
    if InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(new_name):
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 已有相同名稱的播放清單!", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)

    if InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(name):
        InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name).name = new_name
        InstanceManager.mainInstance.save_data()
        embed = wdutils.MessageUtil.get_fancy_embed(":white_check_mark: 成功命名!", color=discord.Colour.green())
        await message.reply(embed=embed, mention_author=False)
    else:
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 播放清單不存在!", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)


@register_command
class PlayPlaylistCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "play-playlist", ["ppl"], "控制類")


@main_command("增加播放清單的內容至待播清單中", PlayPlaylistCommand, name="播放清單名稱")
async def play_playlist(message: Message, name: str) -> None:
    if InstanceManager.mainInstance.data.get_guild(message.guild).has_playlist(name):
        guild_player = InstanceManager.mainInstance.musicManager.get_guild_player_by_message(message)
        playlist = InstanceManager.mainInstance.data.get_guild(message.guild).get_playlist(name)
        if message.guild.voice_client is None:
            InstanceManager.mainInstance.data.get_guild(message.guild).last_vc = message.author.voice.channel.id
            InstanceManager.mainInstance.configsManager.save_data()
            await message.author.voice.channel.connect()
            await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 成功加入語音頻道", discord.Colour.green(),
                                                          message)

        if message.author.voice.channel != guild_player.get_voice_client().channel:
            await wdutils.MessageUtil.reply_fancy_message(
                ":x: 機器人早已在其他頻道! 請使用" + InstanceManager.mainInstance.commandsManager.get_prefix(
                    message.guild) + "leave", discord.Colour.red(), message)
            return
        for track in playlist.tracks:
            await guild_player.add_to_queue(track)
        await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 成功添加 " + len(playlist.tracks).__str__() + " 首歌至待播清單!",
                                                      discord.Colour.green(),
                                                      message)

    else:
        embed = wdutils.MessageUtil.get_fancy_embed(":x: 播放清單不存在!", color=discord.Colour.red())
        await message.reply(embed=embed, mention_author=False)



@register_command
class ReceivePlaylistCommand(WDCommand):
    def __init__(self, commandsManager: CommandsManager) -> None:
        super().__init__(commandsManager, "receive-playlist", ["rpl", "receive"], "播放清單控制")


@main_command("使用播放清單分享金鑰接收播放清單", ReceivePlaylistCommand, name="播放清單名稱")
async def receive_playlist(message: Message, token: str) -> None:
    for guild in InstanceManager.mainInstance.data.guilds:
        if guild.guild_id == message.guild.id:
            for playlist in guild.playlists:
                if playlist.share_id == token:
                    await wdutils.MessageUtil.reply_fancy_message(":x: 您不能分享給自己(本播放清單來自於本群組)", discord.Colour.red(), message)
                    return
        else:
            for playlist in guild.playlists:
                if playlist.share_id == token:
                    cloned = PlayListData()
                    cloned.name = cloned.generate_share_id()
                    cloned.tracks = playlist.tracks
                    InstanceManager.mainInstance.data.get_guild(message.guild).playlists.append(cloned)
                    InstanceManager.mainInstance.save_data()
                    await wdutils.MessageUtil.reply_fancy_message(":white_check_mark: 成功接收 1 個播放清單!", discord.Colour.green(), message)
                    return

