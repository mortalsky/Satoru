import discord
from discord.ext import commands
import asyncio
import os

colour = 0xbf794b

class Owner(commands.Cog, command_attrs=dict(hidden=True)):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.is_owner()
  async def roles(self, ctx):

    emb = discord.Embed(title = 'Take Roles', description = ''':ping_pong: `Updates`''', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await msg.add_reaction('🏓')

  @commands.command()
  async def emoji(self, ctx, emoji: discord.Emoji = None):

    if emoji.animated:
      
      await ctx.send(f'`<a:{emoji.name}:{emoji.id}>` - {emoji} - {emoji.id} - {emoji.url}')

    else:

      await ctx.send(f'`<:{emoji.name}:{emoji.id}>` - {emoji} - {emoji.id} - {emoji.url}')


  @commands.command()
  @commands.is_owner()
  async def load(self, ctx, extension):
    emb = discord.Embed(title = 'Loading...', colour = 0xbf794b)
    emb1 = discord.Embed(title = f'Loaded {extension}!', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    error = discord.Embed(title = f"""UH! There was an error with {extension}! Check this list:
>>> `The extension doesn't exist`
`The extension is already loaded`""", colour = 0xbf794b)
    
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
    error = discord.Embed(title = f"""UH! There was an error with {extension}!
>>> `The extension doesn't exist`
`The extension is not loaded yet`""", colour = 0xbf794b)
    
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
    error = discord.Embed(title = f"""UH! There was an error with {extension}! Check this list:
>>> `The extension doesn't exist`
`The extension is already unloaded`""", colour = 0xbf794b)
    
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

def setup(bot):
  bot.add_cog(Owner(bot))