import discord
import os
import time
from discord.ext import commands

class server_vars:
  def __init__(self, dmstate, dmuser, loop, mode, speed, glob_message):
    self.dmstate = dmstate
    self.dmuser = dmuser
    self.loop = loop
    self.mode = mode
    self.speed = speed
    self.glob_message = glob_message

global serverlist
global server_settings
serverlist = []
server_settings = []

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

  for guild in bot.guilds:
    serverlist.append(guild.id)

  for x in range(len(serverlist)):
    server_settings.append(server_vars(False, '', 0, 0, 0, ''))


@bot.event
async def on_message(message):
  if message.author == bot.user:
      return
  
  try:
    glob = server_settings[serverlist.index(message.guild.id)]
  except:
    user = await bot.fetch_user(int(message.author.id))
    await user.send('ur mom')
    return

  if glob.mode == 1:
    try:
      glob.loop = int(message.content)
      glob.mode = 2
      await message.channel.send("and how fast would u like to spam (it's in milliseconds btw)")
    except:
      await message.channel.send('u need to send an actual number stupid')

  elif glob.mode == 2:
    try:
      glob.speed = int(message.content) / 1000
      glob.mode = 3
      await message.channel.send('do u wanna dm someone or send it here? if u wanna dm, just @ them, and if not, just say "no"')
    except:
      await message.channel.send("i don't understand what you said, repeat?")

  elif glob.mode == 3:
    if message.content.lower() == 'no':
      glob.dmstate = False
      glob.mode = 4
      await message.channel.send("cool, what would u like to spam?")
    else:
      glob.dmstate = True
      glob.dmuser = message.content
      glob.dmuser = glob.dmuser.split('>')[0].split('@')[1]
      glob.dmuser = await bot.fetch_user(int(glob.dmuser))
      await message.channel.send(f"spamming {glob.dmuser} >:)")
      await message.channel.send("and finally, what message would u like to spam?")
      glob.mode = 4

  elif glob.mode == 4:      
    try:
      glob.glob_message = message.content
      await message.channel.send(f"spamming message: {glob.glob_message}")
      print(f'glob.dmstate: {glob.dmstate}, glob.dmuser: {glob.dmuser}, glob.loop: {glob.loop}, glob.mode: {glob.mode}, glob.speed: {glob.speed}, glob.glob_message: {glob.glob_message}')

      for x in range(glob.loop):
        if (glob.dmstate):
          await glob.dmuser.send(glob.glob_message)
          time.sleep(glob.speed)
        else:
          await message.channel.send(glob.glob_message)
          time.sleep(glob.speed)

      glob.mode = 0
    except:
      await message.channel.send("something went very wrong, **fire**?")

  await bot.process_commands(message)

@bot.command()
async def spam(ctx, *args):
  await ctx.send('spammy at ur service! how many times would u like to spam?')
  server_settings[serverlist.index(ctx.message.guild.id)].mode = 1


bot.run('ODg5NzA3Mjk1NDkwMDQ4MDU0.YUlKfQ.kRrCToKu7eMflf-miKW5faYCrRg')
