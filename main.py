import discord
from discord.ext import commands
from discord.ext.commands.core import command
import youtube_dl
import pafy

client = commands.Bot(command_prefix='>') #宣告client變數

class Music2(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.song_queue = {}

        self.setup()

    @commands.Cog.listener()
    async def on_ready(self):
        print('muisc2.py已連接成功')

    def setup(self):
        for guild in self.client.guilds:
            self.song_queue[guild.id] = []

    async def cheak_queue(self, ctx): #列隊
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)


    async def search_song(self, amount, song, get_url=False):
        info = await self.client.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({'formats':"bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song): #播歌
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.client.loop.create_task(self.cheak_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send('**[Beta Version Music Bot]**請輸入要搜尋的歌名')

        await ctx.send('搜尋音樂，這需要花費幾秒鐘')

        info = await self.search_song(5, song)

        await ctx.send('恭喜YYJ，DeBug有進展了 {amount}')

        #embed = discord.Embed(title=f'Test')

        #amount = 0
        #for entry in info["entries"]:
            #embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            #amount += 1

        #embed.set_footer(text=f"顯示第一個 {amount} 結果")
        #await ctx.send(embed=embed)
    
    @commands.command()
    async def j(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("**[Beta Version Music Bot]**你沒有在語音頻道")

        if ctx.voice_client is not None:
            return await ctx.send("**[Beta Version Music Bot]**已在語音頻道")

        await ctx.author.voice.channel.connect() #語音.頻道.加入()
        return await ctx.send("**[Beta Version Music Bot]**加入語音頻道")

    @commands.command()
    async def l(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect() #離開()

        await ctx.send("**[Beta Version Music Bot]**已離開語音頻道")

    @commands.command()
    async def p(self, ctx, *, song=None):
        if song is None:
            return await ctx.send('')

        if ctx.voice_client is None:
            return await ctx.send('')

        if not ('youtube.com/watch?' in song or "https://youtu.be/" in song):
            await ctx.send('**[Beta Version Music Bot]**搜尋音樂，這需要等待幾秒鐘')

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send('**[Beta Version Music Bot]**抱歉我沒找到音樂')

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f'**[Beta Version Music Bot]**我目前在播歌，這首歌已加入隊列')

            else:
                return await ctx.send('**[Beta Version Music Bot]**我只能隊列10首歌')

        await self.play_song(ctx, song)
        await ctx.send(f'現在播放：{song}')

    @commands.command()
    async def q(self, ctx):
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send('目前沒有音樂等待播放')

        embed = discord.Embed(title="音樂隊列", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="(Beta Version)")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send('(Beta Version)我沒在播歌')

        if ctx.author.voice is None:
            return await ctx.send("(Beta Version)你沒連到任何頻道")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send('(Beta Version)我沒播任何音樂')

        poll = discord.Embed(title=f"投票跳過音樂 - {ctx.author.name}#{ctx.author.discriminator}", description="**80% 語音通道必須投票跳過才能通過**", colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="投票在15秒後結束")

        poll_msg = await ctx.send(embed=poll)
        poll_id = poll_msg.id

        poll_msg = await ctx.send(embed=poll) 
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no

        poll_msg = await ctx.channel.fetch_message(poll_id)
        
        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.client:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: 
                skip = True
                embed = discord.Embed(title="成功跳過", description="我懶得打", colour=discord.Colour.green())

        if not skip:
            embed = discord.Embed(title="跳過失敗", description="我懶得打", colour=discord.Colour.red())

        embed.set_footer(text="投票結束")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice.client.stop()
            await self.check_queue(ctx)

    @commands.command()
    async def pa(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("跳過啦")

        ctx.voice_client.pause()
        await ctx.send("當前音樂已被跳過")

    @commands.command()
    async def re(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("我沒有連上語音頻道")

        if not ctx.voice_client.is_paused():
            return await ctx.send("我已經在播歌")
        
        ctx.voice_client.resume()
        await ctx.send("目前音樂已被播放")

def setup(client):
    client.add_cog(Music2(client))