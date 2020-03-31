import discord
from discord.ext import commands 
import json

colour = 0xbf794b

class AutoTriggers(commands.Cog):

  def __init__(self, bot):

    self.bot = bot

  @commands.group(aliases = ["at", "trigger", "triggers"], invoke_without_command = True)
  async def autotrigger(self, ctx, *, trigger):

    "See a response giving a trigger"

    try:

      with open("data/triggers.json", "r") as f:

        l = json.load(f)

      message = discord.utils.escape_mentions(l[str(trigger)]["response"])

      await ctx.send(message)

    except KeyError:

      await ctx.send("Uh! I can't find that auto trigger!")

  @autotrigger.command()
  async def list(self, ctx):

    "See your auto triggers"

    try:

      with open("data/triggers.json", "r") as f:

        l = json.load(f)

      res = ""

      for a in l:

        if l[str(a)]["owner"] == str(ctx.author.id):
          
          res += f"\n`{a}`"

      emb = discord.Embed(description = res, colour = colour)

      await ctx.send(embed = emb)

    except KeyError:

      await ctx.send("You don't have any auto trigger!")

  @autotrigger.command(aliases = ["cr"])
  async def create(self, ctx, trigger, *, response):

    "Create an auto trigger"

    with open("data/triggers.json", "r") as f:

      l = json.load(f)

    l[str(trigger)] = {"response": str(response), "owner": str(ctx.author.id)}

    with open("data/triggers.json", "w") as f:

      json.dump(l, f, indent = 4)

    await ctx.send(f"Done! You can now invoke the trigger doing `autotrigger {trigger}`!")

  @autotrigger.command(aliases = ["del"])
  async def delete(self, ctx, *, trigger):

    "Delete an auto trigger"

    with open("data/triggers.json", "r") as f:

      l = json.load(f)
    
    if l[str(trigger)]["owner"] == str(ctx.author.id):
      
      l.pop(str(trigger))

    with open("data/triggers.json", "w") as f:

      json.dump(l, f, indent = 4)

    await ctx.send(f"Done!")

def setup(bot):
  bot.add_cog(AutoTriggers(bot))