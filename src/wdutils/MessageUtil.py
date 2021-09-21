import discord
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.message import Message



async def send_fancy_message(content: str, color: discord.Colour, channel: TextChannel) -> Message:
    embed = Embed()
    embed.description = content
    embed.colour = color
    return await channel.send(embed=embed)


async def reply_fancy_message(content: str, color: discord.Colour, message: Message) -> Message:
    embed = Embed()
    embed.description = content
    embed.colour = color
    return await message.reply(embed=embed, mention_author=False)

def get_fancy_embed(content: str, color: discord.Colour) -> Embed:
    embed = Embed()
    embed.description = content
    embed.colour = color
    return embed
