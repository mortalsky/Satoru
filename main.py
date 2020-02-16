import discord
from discord.ext import commands, tasks
from discord import Webhook, AsyncWebhookAdapter
import os
from app import keep_alive
import time
import aiohttp
import json
import platform
import psutil

colour = 0xbf794b

bot = commands.AutoShardedBot(command_prefix = commands.when_mentioned_or('e?'))
bot.remove_command('help')
bot.load_extension('jishaku')


@tasks.loop(seconds = 10)
async def stats():

  with open("data/stats.json", "r") as f:

    l = json.load(f)

  l["library"] = discord.__version__
  l["python"] = platform.python_version()
  l["memory"] = psutil.virtual_memory()[2]
  l["cpu"] = psutil.cpu_percent()
  l["running"] = platform.system()
  l["guilds"] = len(bot.guilds)
  l["users"] = len(bot.users)

  with open("data/stats.json", "w") as f:

    json.dump(l, f, indent = 4)

@bot.event
async def on_ready():

  print('Ready as', bot.user)

  await bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.streaming, name = 'e?help', url = 'https://www.twitch.tv/itermosifoni'))

  stats.start()

  with open("data/commands.json", "w") as f:
    
    f.write("{}")

  with open("data/commands.json", "r") as f:

    l = json.load(f)


  for a in bot.commands:

    if not a.hidden:

      if a.name != "jishaku":
        
        l[f"{a.name} {a.signature}"] = a.help
        
        with open("data/commands.json", "w") as f:
          
          json.dump(l, f, indent = 4)
    
@bot.event 
async def on_message(message):

  await bot.process_commands(message)

  with open('data/text.txt', 'a') as f:

    f.write(f'{message.author}: {message.content}\n')

  if message.author == bot.user:
      return

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
token = os.environ.get('secret')
bot.run(token)