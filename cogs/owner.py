import discord
from discord.ext import commands
import asyncio
import os
import json
from datetime import datetime
import traceback
import textwrap
import io
from contextlib import redirect_stdout
import sys
import copy

colour = 0xbf794b

class Owner(commands.Cog, command_attrs = dict(hidden = True)):

  def __init__(self, bot):
    self.bot = bot
    self._last_result = None

  def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

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
    
    try:
      
      self.bot.load_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except Exception as e:

      traceback.print_exc()

      error = discord.Embed(title = f"""UH! There was an error with {extension}!""", description = str(e), colour = 0xbf794b)
      await msg.edit(embed = error)

  @commands.command()
  @commands.is_owner()
  async def reload(self, ctx, extension):
    
    emb = discord.Embed(title = 'Loading...', colour = 0xbf794b)
    emb1 = discord.Embed(title = f'Reloaded {extension}!', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    
    try:
      
      self.bot.unload_extension(f'cogs.{extension}')
      self.bot.load_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except Exception as e:

      traceback.print_exc()

      error = discord.Embed(title = f"""UH! There was an error with {extension}!""", description = str(e), colour = 0xbf794b)
      await msg.edit(embed = error)
    

  @commands.command()
  @commands.is_owner()
  async def unload(self, ctx, extension):
    emb = discord.Embed(title = 'Loading...', colour = 0xbf794b)
    emb1 = discord.Embed(title = f'Unloaded {extension}!', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    
    try:
      
      self.bot.unload_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except Exception as e:

      traceback.print_exc()

      error = discord.Embed(title = f"""UH! There was an error with {extension}!""", description = str(e), colour = 0xbf794b)
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
  async def asyncio(self, ctx, time, times = None, *, thing = None):

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

  @commands.command()
  @commands.is_owner()
  async def nick(self, ctx, *, nick):

    "Nickname the bot"

    await ctx.guild.me.edit(nick = nick)
    await ctx.message.add_reaction("<:greenTick:596576670815879169>")

  @commands.command(hidden=True)
  @commands.is_owner()
  async def eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

def setup(bot):
  bot.add_cog(Owner(bot))