#Snipe bot using discord.py 2.0.0a

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
prefix = "ee"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True



sniped = {}
sniped_edit = {}

class myBot(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {bot.user} (Version: {discord.__version__}")

    async def on_message_delete(self, message):
        sniped[message.channel.id] = [message.content, message.author, message.attachments, message.channel.name, message.created_at]

    async def on_message_edit(self, before, after):
        sniped_edit[before.channel.id] = [before.content, before.author, before.channel.name, before.created_at]


bot = myBot(command_prefix=prefix, intents=intents)





@bot.command()
async def snipe(ctx):
    try:
        contents, author, attch, channel, time = sniped[ctx.channel.id]

        snipe_em = discord.Embed(description=contents, color=discord.Color.blurple(), timestamp=time)
        snipe_em.set_author(name=author, icon_url=author.display_avatar.url)

        if attch:
            if attch[0].proxy_url.endswith('mp4'):
                await ctx.channel.send(embed=snipe_em)
                return await ctx.channel.send(content=attch[0].proxy_url)
            else:
                snipe_em.set_image(url=attch[0].proxy_url)

        snipe_em.set_footer(text=f"Deleted in {channel}")
        return await ctx.channel.send(embed=snipe_em)    
    except KeyError:
        await ctx.send("Nothing to snipe")


@bot.command()
async def snipeedit(ctx):
    try:
        contents, author, channel, time = sniped_edit[ctx.channel.id]

        snipe_ed = discord.Embed(description=contents, color=discord.Color.blurple(), timestamp=time)
        snipe_ed.set_author(name=author, icon_url=author.display_avatar.url)
        snipe_ed.set_footer(text=f"Deleted in {channel}")
        await ctx.channel.send(embed=snipe_ed)
    except KeyError:
        await ctx.channel.send("No recent edits found")



bot.run(TOKEN)