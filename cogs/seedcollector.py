import discord
from discord.ext import commands 
import json
import traceback
import random

class SeedCollector(commands.Cog):

  def __init__(self, bot):

    self.bot = bot 

  @commands.group(invoke_without_command = True)
  async def seed(self, ctx, *, seed: str = None):

    "See a seed"

    with open("data/seed.json", "r") as f:
      l = json.load(f)

    try:
      seed = l[seed]

    except KeyError:

      emb = discord.Embed(description = f"Seed \"**`{seed}`**\" not found.", colour = discord.Colour.red())
      return await ctx.send(embed = emb)

    emb = discord.Embed(title = f"{seed['seed']} | {seed['title']}", description = seed["description"], colour = discord.Colour.green())
    emb.set_footer(text = "Satoru Seed Collector", icon_url = "https://www.lifeisyo.ga/uploads/seed.png")
    emb.set_author(name = seed["author"]["name"], icon_url = seed["author"]["avatar"])
    
    if seed["image"] != "None":

      try:
        emb.set_image(url = seed["image"])

      except Exception as e:
        print(e)
        pass

    await ctx.send(embed = emb)

  @seed.command(usage = "[seed] | [title] | [description] | [image]", aliases = ["cr"])
  async def create(self, ctx, *, info):

    "Create a seed"

    with open("data/seed.json", "r") as f:
      l = json.load(f)

    text = info.split(" | ")

    if len(text) < 3:
      emb = discord.Embed(description = "❌ | Use `seed create <seed>, <title> | <description> | <image (not required)>`", colour = discord.Colour.red())
      return await ctx.send(embed = emb)

    seed = str(text[0])

    title = text[1]
    description = text[2]

    if ctx.message.attachments:
      image = ctx.message.attachments[0].url

    else:
      if len(text) > 3:
        image = text[3]

      else:
        image = "None"

    try:
      seed_ = l[str(seed)]
      emb = discord.Embed(description = "Seed \"**`{seed_}`**\" already exists!", colour = discord.Colour.red())
      return await ctx.send(embed = emb)

    except KeyError:
      pass

    l[str(seed)] = {"title": str(title), "description": str(description), "image": str(image), "seed": seed, "author": {"name": str(ctx.author), "id": int(ctx.author.id), "avatar": str(ctx.author.avatar_url_as(static_format = "png"))}}

    with open("data/seed.json", "w") as f:
      json.dump(l, f, indent = 4)

    emb = discord.Embed(description = f"<:greenTick:596576670815879169> | Seed \"**`{seed}`**\" has been created!", colour = discord.Colour.green())

    await ctx.send(embed = emb)


  @seed.command(aliases = ["del"])
  async def delete(self, ctx, *, seed: str):

    "Delete a seed"

    with open("data/seed.json", "r") as f:
      l = json.load(f)

    try:
      seed_ = l[seed]

    except KeyError:
      emb = discord.Embed(description = f"Seed \"**`{seed}`**\" not found.", colour = discord.Colour.red())
      return await ctx.send(embed = emb)

    id = seed_["author"]["id"]

    if id != ctx.author.id:
      emb = discord.Embed(description = f"You are not the owner of this seed!", colour = discord.Colour.red())
      return await ctx.send(embed = emb)

    else:
      l.pop(str(seed))

    with open("data/seed.json", "w") as f:
      json.dump(l, f, indent=4)

    emb = discord.Embed(description = f"<:greenTick:596576670815879169> | Seed \"**`{seed}`**\" has been deleted!", colour = discord.Colour.green())
    await ctx.send(embed = emb)

  @seed.command()
  async def list(self, ctx):
    
    "See all seeds"

    with open("data/seed.json", "r") as f:
      l = json.load(f)
      
    res = ""

    for a in l:

      res += f"**{a}**: {l[str(a)]['title']}\n"

    if res == "":

      res = "Nothing to see here...."

    emb = discord.Embed(description = res, colour = discord.Colour.green())
    await ctx.send(embed = emb)

def setup(bot):
  bot.add_cog(SeedCollector(bot))