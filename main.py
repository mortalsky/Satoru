import discord
from discord.ext import commands, tasks
import os
from app import keep_alive
import json
import platform
import psutil
from datetime import datetime
import traceback
from dotenv import load_dotenv
from app import keep_alive

colour = 0xbf794b

def get_prefix(bot, message):

  with open("data/prefixes.json", "r") as f:

    json_prefixes = json.load(f)

  try:

    oof = str(json_prefixes[str(message.guild.id)])

    prefix = commands.when_mentioned_or(f"{oof} ", oof)(bot, message)

  except KeyError:

    prefix = commands.when_mentioned_or("e? ", "e?")(bot, message)

  return prefix

bot = commands.AutoShardedBot(command_prefix = get_prefix, description = "Multifunction weeb bot with moderation, fun and more.", case_insensitive = True)
bot.remove_command('help')
bot.load_extension('jishaku')
bot.colour = 0xfffca6

launchtime = datetime.now()

@bot.event
async def on_ready():

  print('Ready as', bot.user)

  await bot.change_presence(status = discord.Status.idle, activity = discord.Streaming(name = "e?help", url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

  f = open("data/commands.txt", "w")

  for a in bot.commands:
    if not a.hidden:
      if a.name != "jishaku":
        try:
          for b in a.commands:
            f.write(f"e?{a.name} {b.name} {b.signature} = {b.help}\n")
        except:
          f.write(f"e?{a.name} {a.signature} = {a.help}\n")
  f.close()

@tasks.loop(seconds = 20)
async def stats():

  with open("data/stats.json", "r") as f:
    l = json.load(f)

  uptime = datetime.now() - launchtime
  hours, remainder = divmod(int(uptime.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)

  l["library"] = discord.__version__
  l["python"] = platform.python_version()
  l["memory"] = psutil.virtual_memory()[2]
  l["cpu"] = psutil.cpu_percent()
  l["running"] = platform.system()
  l["guilds"] = len(bot.guilds)
  l["users"] = len(bot.users)
  l["uptime"] = f"{days}d {hours}h {minutes}m {seconds}s"

  with open("data/stats.json", "w") as f:

    json.dump(l, f, indent = 4)

stats.start()

@bot.check
async def bot_check(ctx):

  if ctx.command.name == "gun":
    
    with open("data/beta.json", "r") as f:
    
      l = json.load(f)

    try:

      if l[str(ctx.author.id)]:
    
        return True

    except KeyError:
      
      return False

  else:

    return True

@bot.event
async def on_command_error(ctx, error):

  emb = discord.Embed(title = "Error", description = f"```css\n{error}\n```\nJoin the [support server](https://discord.gg/w8cbssP) for help.", colour = discord.Colour.red(), timestamp = ctx.message.created_at)
  emb.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)

  if isinstance(error, commands.CommandNotFound):
    return

  if isinstance(error, commands.MissingPermissions):
    if ctx.author.id == 488398758812319745:
      return await ctx.reinvoke()

  if isinstance(error, commands.CommandOnCooldown):
    if ctx.author.id == 488398758812319745:
      return await ctx.reinvoke()

    else:
      return await ctx.send(embed = emb, delete_after = 5)

  if isinstance(error, commands.MaxConcurrencyReached):
    return

  await ctx.send(embed = emb)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

load_dotenv(dotenv_path = ".env")
keep_alive()
token = os.environ.get('secret')
bot.run(token)
