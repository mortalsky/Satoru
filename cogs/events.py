import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import json
from datetime import datetime

colour = 0xbf794b

class Events(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_guild_join(self, guild):

    ch = self.bot.get_channel(607358470907494420)

    emb = discord.Embed(description = f"""<:member_join:596576726163914752> | {self.bot.user.mention} joined **{guild.name}**!
🆔 | {guild.id}
👤 | {guild.owner}
🔢 | {guild.member_count} Members
🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}""", colour = discord.Colour.green())
    emb.set_footer(text = f"{len(self.bot.guilds)} guilds", icon_url = self.bot.user.avatar_url)
    emb.set_thumbnail(url = guild.icon_url)
    if guild.banner:
      emb.set_image(url = guild.banner_url)
      
    await ch.send(embed = emb)

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):

    ch = self.bot.get_channel(607358470907494420)

    emb = discord.Embed(description = f"""👈 | {self.bot.user.mention} left **{guild.name}**!
🆔 | {guild.id}
👤 | {guild.owner}
🔢 | {guild.member_count} Members
🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}""", colour = discord.Colour.red())
    emb.set_footer(text = f"{len(self.bot.guilds)} guilds", icon_url = self.bot.user.avatar_url)
    emb.set_thumbnail(url = guild.icon_url)
    if guild.banner:
      emb.set_image(url = guild.banner_url)
      
    await ch.send(embed = emb)

  @commands.Cog.listener()
  async def on_member_join(self, member):

    guild = member.guild
    channel = self.bot.get_channel(578550625638285332)

    if guild.id == 57854844268786483:

      emb = discord.Embed(title = "Welcome!", description = f"{member.mention}({member} joined {guild.name}! Have fun here!", colour = discord.Colour.green(), timestamp = member.joined_at)
      emb.set_author(name = member, icon_url = member.avatar_url)
      emb.set_thumbnail(url = member.avatar_url)

      await channel.send(embed = emb)

  @commands.Cog.listener()
  async def on_member_remove(self, member):

    guild = member.guild
    channel = self.bot.get_channel(578550625638285332)

    if guild.id == 57854844268786483:

      emb = discord.Embed(title = "Bye Bye!", description = f"{member.mention}({member} left {guild.name}!", colour = discord.Colour.red(), timestamp = datetime.utcnow())
      emb.set_author(name = member, icon_url = member.avatar_url)
      emb.set_thumbnail(url = member.avatar_url)

      await channel.send(embed = emb)
      
def setup(bot):
  bot.add_cog(Events(bot))