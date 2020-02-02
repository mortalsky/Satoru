import discord
from discord.ext import commands

#COLOUR: 0xbf794b

class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def clear(self, ctx, amount = 100):

    """Delete Messages"""
    
    await ctx.message.delete()
    await ctx.channel.purge(limit = amount)

  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member: discord.Member = None, *, reason = None):

    "Ban a member"

    await member.ban(reason = reason, delete_message_days = 2)

    emb = discord.Embed(description = f"✅ | {member.mention} was banned by {ctx.author.mention}", colour = discord.Colour.red())

    await ctx.send(embed = emb)

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member = None, *, reason = None):

    "Kick a member"

    await member.kick(reason = reason)

    emb = discord.Embed(description = f"✅ | {member.mention} was kicked by {ctx.author.mention}", colour = discord.Colour.red())

    await ctx.send(embed = emb)


def setup(bot):
  bot.add_cog(Moderation(bot))