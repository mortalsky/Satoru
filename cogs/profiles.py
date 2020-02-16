import discord
from discord.ext import commands
import json

class Profiles(commands.Cog):

  def __init__(self, bot):

    self.bot = bot

  @commands.group(invoke_without_command = True, aliases = ["pr"])
  async def profile(self, ctx, *, member: discord.Member = None):

    "See a user's profile"

    if not member:
      
      member = ctx.author

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    emb = discord.Embed(timestamp = ctx.message.created_at, colour = discord.Colour.blue())

    if member.nick:

      emb.set_author(name = member.nick, icon_url = member.avatar_url)

    else:

      emb.set_author(name = member.name, icon_url = member.avatar_url)

    try:

      description = l[str(member.id)]["description"]
      
      if l[str(member.id)]["image"]:

        if l[str(member.id)]["image"] != "none":

          image = l[str(member.id)]["image"]

        else:

          image = None

    except KeyError:
      
      description = "Profile not created yet, use `e?profile create`"

      image = None

    emb.description = description

    if image:
      
      emb.set_image(url = image)

    await ctx.send(embed = emb)

  @profile.command()
  async def create(self, ctx):

    "Create your profile"

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    l[str(ctx.author.id)] = {"description": "Not set, use `e?profile description <description>`", "image": "none"}

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

      await ctx.send("You didn't create your profile! Use `e?profile create`.")

  @profile.command(aliases = ["img"])
  async def image(self, ctx, *, image_url = None):

    "Set profile's image"

    with open("data/profiles.json", "r") as f:

      l = json.load(f)

    try:

      if not image_url:

        for a in ctx.message.attachments:

          url = a.url

      else:

        url = image_url
      
      l[str(ctx.author.id)]["image"] = str(url)
      
      with open("data/profiles.json", "w") as f:
        
        json.dump(l, f, indent = 4)

      await ctx.send("Done!")

    except KeyError:

      await ctx.send("You didn't create your profile! Use `e?profile create`.")
      
def setup(bot):
  bot.add_cog(Profiles(bot))