import discord
from discord.ext import commands
import asyncio
import random
import json

#colour = 0xbf794b

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    @commands.command()
    async def gun(self, ctx):

      "Make a gun battle"

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

          with open("data/gun.json", "r") as f:

            l = json.load(f)

          try:
            
            l[str(user.id)] += 1

          except KeyError:

            l[str(user.id)] = 1

          with open("data/gun.json", "w") as f:
            
            json.dump(l, f , indent = 4)

        elif str(reaction.emoji) == "❌":

          if user == ctx.author:

            with open("data/gun.json", "r") as f:
              
              l = json.load(f)

            res = ""

            for a in l:

              res += f"\n<@{a}> - {l[a]}"

            emb2 = discord.Embed(description = res, colour = discord.Colour.green())

            await ctx.send(embed = emb2)

            with open("data/gun.json", "w") as f:
              
              f.write("{}")

            end = True
            

          else:

            msg = await ctx.send(f"{user.mention} only who started the game can stop it!")
            await asyncio.sleep(4)
            await msg.delete()
            
    @commands.command(hidden = True)
    @commands.is_owner()
    async def battle(self, ctx, member: discord.Member = None):

      if member == ctx.author:

        await ctx.send("You can't battle yourself!")
        return

      points = [5, 10, 15, 20, 25]

      xp1 = 150
      xp2 = 150

      ne = discord.Embed(colour = 0xbf794b)

      turn = 1

      def check(m):
        
        return m.author == ctx.author and m.channel == ctx.channel

      if not member:

        await ctx.send(f"[❌] You must specify a member! `{ctx.prefix}battle @member`")
        
      try:

        ne.description = f"{member.mention}, do you accept this battle? (reply with `yes` or `no`)"
        await ctx.send(embed = ne)
        msg = await self.bot.wait_for('message', check=check, timeout = 60)

        if msg.content.lower() == "yes":

          ne.description = "Let's start!"
          await ctx.send(embed = ne)

        elif msg.content.lower() == "no":

          ne.description = "Ok, bye:wave:!"
          await ctx.send(embed = ne)
          return

        else:

          return

      except asyncio.timeOutError:

        ne.description = f"[:clock:] {ctx.author.mention} time out!"

        await ctx.send(embed = ne)

      emb = discord.Embed(title = f"{ctx.author.name} VS {member.name}", colour = discord.Colour.red(), description = f'{ctx.author.mention}\'s life: {xp1}\n{member.mention}\'s life: {xp2}')

      msg = await ctx.send(embed = emb)

      end = False

      while not end:
        
        if turn == 1:

            await ctx.send(f"{ctx.author.mention} do you `attack` or `defend`?")

            m = await self.bot.wait_for('message', check=check, timeout = 60)

            if m.content.lower() == "attack":

              r = random.choice(points)

              xp2 = (xp2 - int(r))

              emb.description += f"\n{ctx.author.mention} attacked {member.mention} who lost {r} points!"

              await msg.delete()
              msg = await ctx.send(embed = emb)

              turn = 2

            elif m.content.lower() == "defend":

              r = random.choice(points)

              xp1 = (xp1 + int(r))

              emb.description += f"\n{ctx.author.mention} defended, xps increment of {r}!"

              await ctx.send(embed = emb)

              turn = 2
              
        elif turn == 2: 

            await ctx.send(f"{member.mention} do you `attack` or `defend`?")

            m = await self.bot.wait_for('message', check=check, timeout = 60)

            if m.content == "attack":

              r = random.choice(points)

              xp1 = (xp1 - int(r))

              emb.description += f"\n{member.mention} attacked {ctx.author.mention} who lost {r} points!"

              await msg.delete()
              msg = await ctx.send(embed = emb)

              turn = 2

            elif m.content == "defend":

              r = random.choice(points)

              xp2 = (xp2 + int(r))

              emb.description += f"\n{member.mention.mention} defended, xps increment of {r}!"

              await ctx.send(embed = emb)

              turn = 1

      


        


def setup(bot):
    bot.add_cog(Battle(bot))