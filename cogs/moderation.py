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

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def mute(self, ctx, member: discord.Member = None, *, reason = None):

    "Mute a member"

    r = discord.utils.get(ctx.guild.roles, name = "Muted")

    if not r:

      r = await ctx.guild.create_role(name = "Muted")

    await member.add_roles(r, reason = reason)

    emb = discord.Embed(description = f"✅ | {member.mention} was muted by {ctx.author.mention}", colour = discord.Colour.red())

    await ctx.send(embed = emb)

    try:
      
      for a in ctx.guild.channels:
        
        await a.set_permissions(r, send_messages = False)

    except:

      return


  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def unmute(self, ctx, member: discord.Member = None):

    "Unmute a member"

    r = discord.utils.get(ctx.guild.roles, name = "Muted")

    await member.remove_roles(r)

    emb = discord.Embed(description = f"✅ | {member.mention} was unmuted by {ctx.author.mention}", colour = discord.Colour.green())

    await ctx.send(embed = emb)

def setup(bot):
  bot.add_cog(Moderation(bot))