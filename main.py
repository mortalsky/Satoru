import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import time

colour = 0xbf794b

bot = commands.Bot(command_prefix = commands.when_mentioned_or('e?'))
bot.remove_command('help')
bot.load_extension('jishaku')

launch_time = time.gmtime()

@bot.event
async def on_ready():
  print('Ready as', bot.user)
  await bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.streaming, name = 'e?help', url = 'https://www.twitch.tv/itermosifoni'))

@bot.event 
async def on_message(message):

  await bot.process_commands(message)

  with open('text.txt', 'a') as f:

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

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
token = os.environ.get('secret')
bot.run(token)