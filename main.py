import discord
from discord.ext import commands
from time import sleep
import os
from dotenv import load_dotenv
from webserver import keep_alive

load_dotenv() #As the name suggets, it loads the dotenv file that contains the bot's token
TOKEN = os.getenv('TOKEN') # "os.getenv()" looks for the TOKEN key in the .env and uses the value (the bot's token) 

prefix = "ee"

intents = discord.Intents.default()
intents.message_content = True
#This gives access to the message intent that must be switched on in the developer portal


sniped = {}
sniped_edit = {}
#These dictionaries store the deleted messages that our on_message events capture

class myBot(commands.Bot): #Being used as an event handler, but this class isn't needed for the bot to work overall (You'd just have to make the necessary changes). It's just more organized.
  async def on_ready(self):
      print(f"Logged in as {bot.user} (Version: {discord.__version__}") #When the bot is online this function prints.

  async def on_message_delete(self, message):
        if message.author == self.user:
            return # Ignore if the message was deleted by the bot itself
        
        sniped[message.channel.id] = [
            message.content, message.author, message.attachments, message.stickers, message.channel.name, message.created_at
        ]

  async def on_message_edit(self, before, after):
        sniped_edit[before.channel.id] = [
           before.content, before.author, after.content, before.channel.name, before.created_at
]

bot = myBot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
  print("Bot is up and ready!")
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)") #prints how many commands the bot sees
  except Exception as e:
    print(e)   

@bot.tree.command(name="snipe", description="will snipe the last message deleted")
async def snipe(interaction: discord.Interaction):
  try:
    contents, target, attch, stickers, channel, time = sniped[interaction.channel.id]
  except KeyError:
    return await interaction.response.send_message("Nothing to snipe")

  snipe_em = discord.Embed(description=contents, color=discord.Color.blurple(), timestamp=time) #this is the embeded message that the bot will send
  snipe_em.set_author(name=target.name, icon_url=target.display_avatar.url) #change ".name" to "display_name" if you want the bot to show the name and not the discord @

  attachment_url = None
  if attch:  # If an attachment is found (img/video) then it will adjust the embed accordingly.
    attachment = attch[0]
    if attachment.proxy_url.endswith(('mp4', 'mov')):
      attachment_url = attachment.proxy_url
      snipe_em.description += f"\n Video found! link posted below" #when a video is found it will send this message
    else:
      snipe_em.set_image(url=attachment.proxy_url)

  if stickers:
    for sticker in stickers:
      snipe_em.set_image(url=sticker.url)  # sets the embed images as the sticker that was sent

  snipe_em.set_footer(text=f"Deleted in {channel}")
  await interaction.response.send_message(embed=snipe_em)  # Send embed with message content and author info

  if attachment_url:
    await interaction.channel.send(attachment_url)  # Send the video link separately (larger files won't embed but link will still be sent)

@bot.tree.command(name="esnipe", description="will snipe the last message edited")
async def snipeedit(interaction: discord.Interaction):
    try:
        original, author, edited, channel, time = sniped_edit[interaction.channel.id]
    except KeyError:
        return await interaction.response.send_message("No recent edits found")

    snipe_embed = discord.Embed(color=discord.Color.blurple(), timestamp=time)
    snipe_embed.set_author(name=author.name, icon_url=author.display_avatar.url)
    snipe_embed.set_footer(text=f"Message edited in {channel}")

    # Add fields for original and edited content
    snipe_embed.add_field(name="Original Content", value=original, inline=False)
    snipe_embed.add_field(name="Edited to", value=edited, inline=False)

    await interaction.response.send_message(embed=snipe_embed)

try:
    keep_alive()
    bot.run(TOKEN)
except discord.errors.HTTPException:
  os.system("echo RATELIMITED, TRYING AGAIN")
  sleep(25)
  os.system("kill 1")