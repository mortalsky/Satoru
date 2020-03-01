import discord
from discord.ext import commands
import asyncio
import os
import json
from datetime import datetime

colour = 0xbf794b

class Owner(commands.Cog, command_attrs=dict(hidden=True)):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_completion(self, ctx):

    with open("data/logs.json", "r") as f:

      l = json.load(f)

    l.append(f"{ctx.author} :: {ctx.command}")

    with open("data/logs.json", "w") as f:

      json.dump(l, f, indent = 4)

  @commands.command()
  @commands.is_owner()
  async def last(self, ctx, commands = 5):

    "See last commands run by the users"

    with open("data/logs.json", "r") as f:

      l = json.load(f)

    num = len(l)

    res = ""

    for a in range(commands):

      num -= 1
      res += f"\n{l[num]}"

    emb = discord.Embed(title = f"Last {commands} commands ran", description = f"```prolog\n{res}\n```", colour = discord.Colour.blurple())
    await ctx.send(embed = emb)

  @commands.command()
  async def emoji(self, ctx, emoji: discord.Emoji = None):

    if emoji.animated:
      
      await ctx.send(f'`<a:{emoji.name}:{emoji.id}>` - {emoji} - {emoji.id} - {emoji.url}')

    else:

      await ctx.send(f'`<:{emoji.name}:{emoji.id}>` - {emoji} - {emoji.id} - {emoji.url}')

  @commands.group(hidden = True, invoke_without_command = True)
  @commands.is_owner()
  async def beta(self, ctx):

    with open("data/beta.json", "r") as f:

      l = json.load(f)

    users = ""

    for a in l:

      u = self.bot.get_user(int(a))

      users += f"\n**`{u}`**"

    emb = discord.Embed(title = "Beta Users", description = users, colour = colour)

    await ctx.send(embed = emb)

  @beta.command(hidden = True)
  @commands.is_owner()
  async def add(self, ctx, *, user: discord.User):

    with open("data/beta.json", "r") as f:

      l = json.load(f)

    l[str(user.id)] = "True"

    with open("data/beta.json", "w") as f:

      json.dump(l, f, indent = 4)

    await ctx.send(f"Added {user.name} to the beta list.")

  @beta.command(hidden = True)
  @commands.is_owner()
  async def remove(self, ctx, *, user: discord.User):

    with open("data/beta.json", "r") as f:

      l = json.load(f)

    l.pop(str(user.id))

    with open("data/beta.json", "w") as f:

      json.dump(l, f, indent = 4)

    await ctx.send(f"Removed {user.name} to the beta list.")

  @commands.command()
  @commands.is_owner()
  async def load(self, ctx, extension):
    emb = discord.Embed(title = 'Loading...', colour = 0xbf794b)
    emb1 = discord.Embed(title = f'Loaded {extension}!', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    error = discord.Embed(title = f"""UH! There was an error with {extension}!""", colour = 0xbf794b)
    
    try:
      
      self.bot.load_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except:
      
      await msg.edit(embed = error)

  @commands.command()
  @commands.is_owner()
  async def reload(self, ctx, extension):
    
    emb = discord.Embed(title = 'Loading...', colour = 0xbf794b)
    emb1 = discord.Embed(title = f'Reloaded {extension}!', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    error = discord.Embed(title = f"""UH! There was an error with {extension}!""", colour = 0xbf794b)
    
    try:
      
      self.bot.unload_extension(f'cogs.{extension}')
      self.bot.load_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except:
      
      await msg.edit(embed = error)
    

  @commands.command()
  @commands.is_owner()
  async def unload(self, ctx, extension):
    emb = discord.Embed(title = 'Loading...', colour = 0xbf794b)
    emb1 = discord.Embed(title = f'Unloaded {extension}!', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    error = discord.Embed(title = f"""UH! There was an error with {extension}!""", colour = 0xbf794b)
    
    try:
      
      self.bot.unload_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except:
      
      await msg.edit(embed = error)

  @commands.command()
  @commands.is_owner()
  async def install(self, ctx, package):

    "Upgrade a package"

    await ctx.message.add_reaction("<a:typing:597589448607399949>")

    async with ctx.typing():

      os.system(f"pip install {package}")

    await ctx.message.remove_reaction("<a:typing:597589448607399949>", self.bot.user)
    await ctx.message.add_reaction("<:greenTick:596576670815879169>")

    await ctx.send(f"Installed {package}!")

  @commands.command()
  @commands.is_owner()
  async def upgrade(self, ctx, package):

    "Upgrade a package"

    await ctx.message.add_reaction("<a:typing:597589448607399949>")

    async with ctx.typing():
      
      os.system(f"pip install --upgrade {package}")

    await ctx.message.remove_reaction("<a:typing:597589448607399949>", self.bot.user)
    await ctx.message.add_reaction("<:greenTick:596576670815879169>")
    
    await ctx.send(f"Upgraded {package}!")

  @commands.command()
  @commands.is_owner()
  async def uninstall(self, ctx, package):

    "Upgrade a package"

    await ctx.message.add_reaction("<a:typing:597589448607399949>")

    async with ctx.typing():

      os.system(f"pip uninstall {package}")

    await ctx.message.remove_reaction("<a:typing:597589448607399949>", self.bot.user)
    await ctx.message.add_reaction("<:greenTick:596576670815879169>")

    await ctx.send(f"Uninstalled {package}!")


  @commands.command()
  @commands.is_owner()
  async def asyncio(self, ctx, time, times = None, thing = None):

    "Sleep little Satoru"

    if not times:

      times = 1

    if thing:

      thing = f"**{thing}**"

    else:

      thing = " "

    await ctx.message.add_reaction("\U0001f44d")

    for a in range(int(times)):
      
      await asyncio.sleep(int(time))

    before = ctx.message.created_at
    
    await ctx.send(f"{ctx.author.mention}, at `{before.strftime('%d %b %Y - %I:%M %p')}` {thing}")

def setup(bot):
  bot.add_cog(Owner(bot))