#Snipe bot using discord.py 1.7.3

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
from webserver import keep_alive

load_dotenv() #As the name suggets, it loads the dotenv file that contains the bot's token
TOKEN = os.getenv('TOKEN') # "os.getenv()" looks for the TOKEN key in the .env and uses the value (the bot's token) 

prefix = "ee"

intents = discord.Intents.default()
intents.messages = True
#This gives access to the message intent that must be switched on in the developer portal


sniped = {}
sniped_edit = {}

#These dictionaries store the deleted messages that our on_message events capture



class myBot(commands.Bot): #Being used as an event handler, but this class isn't needed for the bot to work overall (You'd just have to make the necessary changes). It's just more organized.
  async def on_ready(self):
      print(f"Logged in as {bot.user} (Version: {discord.__version__}") #When the bot is online this function prints.

  async def on_message_delete(self, message): #When a message is deleted it looks at the channel that it happened in, the user who deleted it, (along with the other specifications) and appends it to the "sniped" dictionary.
      sniped[message.channel.id] = [
          message.content, message.author, message.attachments,
          message.channel.name, message.created_at
      ]

  async def on_message_edit(self, before, after): #Same concept as on_message_delete
      sniped_edit[before.channel.id] = [
          before.content, before.author, before.channel.name,
          before.created_at
      ]


bot = myBot(command_prefix=prefix, intents=intents)


@bot.command()
async def snipe(ctx):
    try:
        contents, target, attch, channel, time = sniped[ctx.channel.id]
    except KeyError: #If no one has deleted a message or the cache is reset, then the bot prints "Nothing to snipe" and stops.
        return await ctx.send("Nothing to snipe")

    snipe_em = discord.Embed(description=contents,
                             color=discord.Color.blurple(),
                             timestamp=time)
    snipe_em.set_author(name=target, icon_url=target.avatar_url)

    if attch: #If an attachment is found (img/video) then it will adjust to the embed accordingly.
        if attch[0].proxy_url.endswith('mp4'):
            await ctx.send(embed=snipe_em)
            return await ctx.send(content=attch[0].proxy_url)
        else:
            snipe_em.set_image(url=attch[0].proxy_url)

    snipe_em.set_footer(text=f"Deleted in {channel}")
    await ctx.send(embed=snipe_em)


@bot.command()
async def snipeedit(ctx):  #Same concept as snipe
    try:
        contents, target, channel, time = sniped_edit[ctx.channel.id]
    except KeyError:
        return await ctx.send("No recent edits found")

    snipe_ed = discord.Embed(description=contents,
                             color=discord.Color.blurple(),
                             timestamp=time)
    snipe_ed.set_author(name=target, icon_url=target.avatar_url)
    snipe_ed.set_footer(text=f"Deleted in {channel}")
    await ctx.send(embed=snipe_ed)

keep_alive()
bot.run(TOKEN)
