#Snipe bot using discord.py 1.7.3

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv



load_dotenv()
TOKEN = os.getenv("TOKEN")
prefix = "ee"

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (Version: {discord.__version__})")



sniped = {}


@bot.listen()
async def on_message_delete(message):
  sniped[message.channel.id] = [message.content, message.author, message.channel.name, message.attachments, message.created_at]



@bot.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, attch, time = sniped[ctx.channel.id]

        sniped_embed = discord.Embed(description=contents, color=discord.Color.blurple(), timestamp=time)
        sniped_embed.set_author(name=f'{author.name}#{author.discriminator}',icon_url=author.avatar_url)
    
        if attch:
            if attch[0].proxy_url.endswith("mp4"):
                await ctx.channel.send(embed=sniped_embed)
                return await ctx.channel.send(content=attch[0].proxy_url)
            else:
                sniped_embed.set_image(url=attch[0].proxy_url)

        sniped_embed.set_footer(text=f'deleted in {channel_name} ')
        return await ctx.channel.send(embed=sniped_embed)
    except KeyError:
        await ctx.send("Nothing to snipe.")




sniped_edit = {}

@bot.listen()
async def on_message_edit(before, after):
    sniped_edit[before.channel.id] =  [before.content, before.author, before.channel.name, before.created_at]



@bot.command()
async def snipeedit(ctx):
    try:
        contents, author, channel_name, time = sniped_edit[ctx.channel.id]

        sniped_ed = discord.Embed(description=contents, color=discord.Color.blurple(), timestamp=time)
        sniped_ed.set_author(name=author, icon_url=author.avatar_url)
        sniped_ed.set_footer(text=f"deleted in {channel_name}")

        await ctx.channel.send(embed=sniped_ed)
    except KeyError:
        await ctx.send("Nothing to snipe.")



bot.run(TOKEN)