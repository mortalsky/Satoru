import discord
from discord.ext import commands
import json
import random

colour = 0xbf794b

class Profiles(commands.Cog):

  def __init__(self, bot):

    self.bot = bot

  @commands.group(invoke_without_command = True, aliases = ["pr"])
  async def profile(self, ctx, *, member: discord.User = None):

    "See a user's profile"

    if not member:
      
      member = ctx.author

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    emb = discord.Embed(timestamp = ctx.message.created_at, colour = discord.Colour.blue())

    emb.set_author(name = member.name, icon_url = member.avatar_url)

    try:

      description = l[str(member.id)]["description"]
      
      if l[str(member.id)]["image"]:

        if l[str(member.id)]["image"] != "none":

          if l[str(member.id)]["image"] == "None":

            image = None

          else:

            image = l[str(member.id)]["image"]

        else:

          image = None

    except KeyError:
      
      description = "Profile not created yet, use `profile create`"

      image = None

    emb.description = description

    try:

      emb.add_field(name = "Total Money", value = f"{l[str(member.id)]['money']}💸")

    except KeyError:

      pass

    if image:
      
      emb.set_image(url = image)

    await ctx.send(embed = emb)

  @profile.command()
  async def list(self, ctx):

    "See who has a profile in the actual guild"

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    res = ""

    for a in l:

      u = self.bot.get_user(int(a))

      if u in ctx.guild.members:
        
        res += f"\n{u}"

    emb = discord.Embed(description = f"```prolog\n{res}\n```", colour = colour)
    emb.set_author(name = f"Users in {ctx.guild.name}", icon_url = ctx.guild.icon_url)

    await ctx.send(embed = emb)

  @profile.command()
  async def create(self, ctx):

    "Create your profile"

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    l[str(ctx.author.id)] = {"description": "Not set, use `profile description <description>`", "image": "none", "money": 0}

    with open("data/profiles.json", "w") as f:

      json.dump(l, f, indent = 4)

    await ctx.send("Done! You can now set your description with `e?profile description <your description>` and your image with `e?profile image <image url>`")

  @profile.command()
  async def delete(self, ctx):

    "Delete your profile"

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    l.pop(str(ctx.author.id))

    with open("data/profiles.json", "w") as f:

      json.dump(l, f)

    await ctx.send("Done!")


  @profile.command(aliases = ["desc"])
  async def description(self, ctx, *, description):

    "Set profile's description"

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    try:
      
      l[str(ctx.author.id)]["description"] = str(description)
      
      with open("data/profiles.json", "w") as f:
        
        json.dump(l, f, indent = 4)

      await ctx.send("Done!")

    except KeyError:

      await ctx.send("You didn't create your profile! Use `profile create`.")

  @profile.command(aliases = ["img"])
  async def image(self, ctx, *, image_url = None):

    "Set profile's image, use `profile image remove` to remove the image"

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    try:

      if not image_url:

        for a in ctx.message.attachments:

          url = a.url

      else:

        if image_url.lower() == "remove":

          url = None

        else:
          
          url = image_url
      
      l[str(ctx.author.id)]["image"] = str(url)
      
      with open("data/profiles.json", "w") as f:
        
        json.dump(l, f, indent = 4)

      await ctx.send("Done!")

    except KeyError:

      await ctx.send("You didn't create your profile! Use `profile create`.")

  @commands.command()
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def work(self, ctx):

    "Work and earn money"

    random_money = random.choice(range(5, 100))

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    try:

      l[str(ctx.author.id)]["money"] += random_money

      with open("data/profiles.json", "w") as f:

        json.dump(l, f, indent = 4)

    except KeyError:

      return await ctx.send("You didn't create your profile! Use `profile create`.")

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    emb = discord.Embed(title = "Good Work!", description = f"You earned **{random_money}💸** and you now have a total of **{l[str(ctx.author.id)]['money']}💸** money.", colour = discord.Colour.green(), timestamp = ctx.message.created_at)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)

    await ctx.send(embed = emb)

  @commands.command(aliases = ["lb"])
  async def leaderboard(self, ctx):

    "See users lb"

    users = []

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    lb = sorted(l, key=lambda x : l[x].get('money', 0), reverse=True)

    res = ""

    for a in lb:

      u = self.bot.get_user(int(a))

      res += f"\n`{u}` - **{l[str(a)]['money']}💸**"

    emb = discord.Embed(title = "Leaderboard", description = res, colour = discord.Colour.blurple(), timestamp = ctx.message.created_at)

    await ctx.send(embed = emb) 

def setup(bot):
  bot.add_cog(Profiles(bot))