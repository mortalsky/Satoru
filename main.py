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

launch_time = time.gmtime()

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

@bot.command()
async def uptime(ctx):

  "See bot uptime"

  days = round(time.gmtime().tm_mday - launch_time.tm_mday)

  hour = round(time.gmtime().tm_hour - launch_time.tm_hour)

  min = round(time.gmtime().tm_min - launch_time.tm_min )

  sec = round(time.gmtime().tm_sec - launch_time.tm_sec)

  emb = discord.Embed(description = f":clock: | {days} days {hour} hours {min} mins {sec} secs", colour = colour)

  await ctx.send(embed = emb)

@bot.event
async def on_command_error(ctx, error):

      c = bot.get_command(str(ctx.command.name))

      emb = discord.Embed(description = f"""📛 | **ERROR**
⌨️ | {c.name} {c.signature}
👤 | {ctx.author}
⁉️ | ```css\n{error}\n```""", timestamp = ctx.message.created_at, colour = discord.Colour.red())

      async with aiohttp.ClientSession() as session:
          
        webhook = Webhook.from_url("https://discordapp.com/api/webhooks/676549434368196642/fLQCMUQfVEpTYZK_HuwGEGwgeFH1n4bNHuocJs8wX40-b0ngdA9oMQ0SEt8BM7ufxmi3", adapter=AsyncWebhookAdapter(session))
        
        await webhook.send(embed = emb)
        
      emb0 = discord.Embed(description = f"❌ | {error}", colour = discord.Colour.red())

      await ctx.send(embed = emb0)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
token = os.environ.get('secret')
bot.run(token)