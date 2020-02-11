import discord
from discord.ext import commands
import asyncio

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




def setup(bot):
  bot.add_cog(Owner(bot))