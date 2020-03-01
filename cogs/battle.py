import discord
from discord.ext import commands
import asyncio
import random
import time

colour = 0xbf794b

class Battle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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

        await asyncio.sleep(1)
        
        reaction, user = await self.bot.wait_for('reaction_add', check = check)
        
        if str(reaction.emoji) == "🔫":

          try:
            
            l[str(user.id)] += 1

          except KeyError:

            l[str(user.id)] = 1

        elif str(reaction.emoji) == "❌":

          if user == ctx.author:

            res = ""
            
            for a in l:

              res += f"\n<@{a}> - {l[a]}"

            emb2 = discord.Embed(description = res, colour = discord.Colour.green())

            await ctx.send(embed = emb2)

            end = True

    @commands.command(aliases = ["hg"])
    async def hungergames(self, ctx, *, members = None):

      "Create an Hunger Game! If members is none, bot will choose 8 random members."

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

      if members:

        x = members.split(" ")

      else:

        x = ctx.guild.members

      try:

        players = random.sample(x, 8)

      except ValueError:

        return await ctx.send("Min 8 players!")
      
      emb = discord.Embed(colour = discord.Colour.blurple(), title = "Hunger Games")

      emb.description = f"""
{players[0]} 
`----- VS -----`     
{players[1]}  
                  
{players[2]}
`----- VS -----`
{players[3]}
                  
{players[4]}
`----- VS -----`     
{players[5]}    
                  
{players[6]}
`----- VS -----`    
{players[7]}   
"""

      msg = await ctx.send(embed = emb)

      await asyncio.sleep(2)

      onevtwo = random.choice([players[0], players[1]])
      threevfour = random.choice([players[2], players[3]])
      fivevsix = random.choice([players[4], players[5]])
      sevenveight = random.choice([players[6], players[7]])

      emb.description = f"""
{onevtwo}     
`----- VS -----`          
{threevfour}        
                 
{fivevsix}
----- VS -----
{sevenveight}
"""

      await msg.edit(embed = emb)

      await asyncio.sleep(2)

      onevthree = random.choice([onevtwo, threevfour])
      fivevseven = random.choice([fivevsix, sevenveight])

      emb.description = f"""
{onevthree}

`----- VS -----`       
                  
{fivevseven}
"""
      await msg.edit(embed = emb)

      await asyncio.sleep(2)

      winner = random.choice([onevthree, fivevseven])

      emb.description = f"""
**👑 {winner} 👑**
"""
      await msg.edit(embed = emb)

def setup(bot):
    bot.add_cog(Battle(bot))