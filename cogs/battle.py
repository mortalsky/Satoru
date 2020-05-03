import discord
from discord.ext import commands
import asyncio
import random
import json
from discord.ext.commands.cooldowns import BucketType
import os

colour = 0xbf794b

class Battle(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.hg_playing = []

  @commands.command()
  async def gun(self, ctx):

    "Make a gun battle"

    l = {}

    end = False

    emb = discord.Embed(description = "Who react with :gun: more times wins!", colour = discord.Colour.green())

    msg = await ctx.send(embed = emb)

    await msg.add_reaction("🔫")
    await msg.add_reaction("❌")

    def check(reaction, user):
      
      return user != self.bot.user

    while not end:
      
      reaction, user = await self.bot.wait_for('reaction_add', check = check)
      
      if str(reaction.emoji) == "🔫":

        try:
          
          l[str(user.id)] += 1

        except KeyError:

          l[str(user.id)] = 1

      elif str(reaction.emoji) == "❌":

        if user == ctx.author:

          res = ""

          lb = sorted(l, key=lambda x : l[x], reverse=True)

          counter = 0

          for a in lb:

            counter += 1

            res += f"\n{counter} | <@{a}> - {l[a]}"

          emb2 = discord.Embed(description = res, colour = discord.Colour.green())

          await ctx.send(embed = emb2)

          end = True

  @commands.command(aliases = ["hungergame", "hg"])
  async def hungergames(self, ctx, *, members = None):

    "Create an Hunger Game! If members is none, bot will choose 8 random members. Use `,` to separate players, Ex. `hungergames lmao, lel, lol....`"

    # 1 --
    #     |---
    # 2 --    |
    #         |----             I spent like 30 mins
    # 3 --    |    |            only for this shitty
    #     |---     |            comment, lmao.
    # 4 --         |         
    #              |----- 0       
    # 5 --         |
    #     |---     |
    # 6 --    |    |
    #         |--- 
    # 7 --    |
    #     |---
    # 8 --

    if not ctx.channel.id in self.hg_playing:

      pass

    else:

      return await ctx.send("I'm already playing a game in this channel!", delete_after = 5)

    self.hg_playing.append(ctx.channel.id)

    if members:

      x = members.split(",")

    else:

      x = ctx.guild.members

    try:

      players = random.sample(x, 8)

    except ValueError:

      self.hg_playing.remove(ctx.channel.id)
      return await ctx.send("Min 8 players!")
    
    emb = discord.Embed(colour = discord.Colour.blurple(), title = "Hunger Games")

    emb.description = f"""
**{players[0]}** 
`----- VS -----`     
**{players[1]}**  
                
**{players[2]}**
`----- VS -----`
**{players[3]}**
                
**{players[4]}**
`----- VS -----`     
**{players[5]}**    
                
**{players[6]}**
`----- VS -----`    
**{players[7]}**     
"""

    msg = await ctx.send(embed = emb)

    await asyncio.sleep(2)

    onevtwo = random.choice([players[0], players[1]])
    threevfour = random.choice([players[2], players[3]])
    fivevsix = random.choice([players[4], players[5]])
    sevenveight = random.choice([players[6], players[7]])

    emb.description = f"""
**{onevtwo}**     
`----- VS -----`          
**{threevfour}**        
              
**{fivevsix}**
`----- VS -----`   
**{sevenveight}**
"""

    await msg.edit(embed = emb)

    await asyncio.sleep(2)

    onevthree = random.choice([onevtwo, threevfour])
    fivevseven = random.choice([fivevsix, sevenveight])

    emb.description = f"""
**{onevthree}**

`----- VS -----`       
                
**{fivevseven}**
"""
    await msg.edit(embed = emb)

    await asyncio.sleep(2)

    winner = random.choice([onevthree, fivevseven])

    emb.description = f"""
**👑 {winner} 👑**
"""
    await msg.edit(embed = emb)
    
    self.hg_playing.remove(ctx.channel.id)

  @commands.group(invoke_without_command = True, aliases = ["egg", "eggs", "cookies"])
  @commands.cooldown(1, 5, BucketType.user) 
  async def cookie(self, ctx):

    "COOKIE CHALLENGE"

    emb = discord.Embed(description = "First one to take the cookie wins🍪!", colour = 0xa8603d)
    msg = await ctx.send(embed = emb)
    await msg.add_reaction("🍪")

    def check(reaction, user):
      return user != self.bot.user and str(reaction.emoji) == '🍪' and reaction.message.id == msg.id

    msg0 = await self.bot.wait_for("reaction_add", check = check)

    emb.description = f"{msg0[1].mention} won and ate the cookie🍪!"

    await msg.edit(embed = emb)

    with open("data/cookie.json", "r") as f:

      l = json.load(f)

    try:
      
      l[str(msg0[1].id)] += 1

    except KeyError:

      l[str(msg0[1].id)] = 1

    with open("data/cookie.json", "w") as f:

      json.dump(l, f, indent = 4)

  @cookie.command(aliases = ["lb", "top"])
  async def leaderboard(self, ctx):

    "Top Cookie users"

    with open("data/cookie.json", "r") as f:

      l = json.load(f)
    
    lb = sorted(l, key=lambda x : l[x], reverse=True)

    res = ""

    counter = 0

    for a in lb:

      counter += 1

      if counter > 10:

        pass
      
      else:
        
        u = self.bot.get_user(int(a))

        res += f"\n**{counter}.** `{u}` - **{l[str(a)]} 🍪**"

    emb = discord.Embed(description = res, colour = 0xa8603d)

    await ctx.send(embed = emb)
    
  @cookie.command(aliases = ["stats", "info"])
  async def stat(self, ctx, *, user: discord.User = None):
    
    if not user:

      user = ctx.author

    with open("data/cookie.json", "r") as f:

      l = json.load(f)

    cookies = l[str(user.id)]

    emb = discord.Embed(description = f"**{cookies}** Cookies 🍪!", colour = 0xa8603d)
    emb.set_author(name = user.name, icon_url = user.avatar_url_as(static_format="png"))

    await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(Battle(bot))