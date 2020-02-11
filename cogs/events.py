import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

colour = 0xbf794b

class Events(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_guild_join(self, guild):

    emb = discord.Embed(description = f"""<:member_join:596576726163914752> | {self.bot.user.mention} joined **{guild.name}**!
🆔 | {guild.id}
👤 | {guild.owner}
🔢 | {guild.member_count}
🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}""", colour = discord.Colour.green())
    emb.set_footer(text = f"{len(self.bot.guilds)} guilds", icon_url = self.bot.user.avatar_url)
    emb.set_thumbnail(url = guild.icon_url)
    if guild.banner:
      emb.set_image(url = guild.banner_url)
      
    async with aiohttp.ClientSession() as session:

      with open("data/private.json", "r") as f:

        l = json.load(f)
      
      webhook = Webhook.from_url(l["webhooks"]["join"], adapter=AsyncWebhookAdapter(session))
      await webhook.send(embed = emb)

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):

    emb = discord.Embed(description = f"""👈 | {self.bot.user.mention} left **{guild.name}**!
🆔 | {guild.id}
👤 | {guild.owner}
🔢 | {guild.member_count}
🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}""", colour = discord.Colour.red())
    emb.set_footer(text = f"{len(self.bot.guilds)} guilds", icon_url = self.bot.user.avatar_url)
    emb.set_thumbnail(url = guild.icon_url)
    if guild.banner:
      emb.set_image(url = guild.banner_url)
      
    async with aiohttp.ClientSession() as session:
      
      with open("data/private.json", "r") as f:

        l = json.load(f)
      
      webhook = Webhook.from_url(l["webhooks"]["join"], adapter=AsyncWebhookAdapter(session))
      await webhook.send(embed = emb)

    @commands.Cog.listener()
    async def on_command_error(ctx, error):

      emb = discord.Embed(description = f"""📛 | **ERROR**
<a:typing:597589448607399949> | {ctx.invoke}
👤 | {ctx.author}
⁉️ | ```css\n{error}\n```""", timestamp = ctx.message.created_at, colour = discord.Colour.red())

      async with aiohttp.ClientSession() as session:
        
        with open("data/private.json", "r") as f:
          
          l = json.load(f)
          
        webhook = Webhook.from_url(l["webhooks"]["errors"], adapter=AsyncWebhookAdapter(session))
        
        await webhook.send(embed = emb)

def setup(bot):
  bot.add_cog(Events(bot))