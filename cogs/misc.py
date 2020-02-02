import discord
from discord.ext import commands
import aiohttp

colour = 0xbf794b

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["fb"])
    async def feedback(self, ctx, *, feedback):

      "Send a feedback to the bot or suggest a new command"

      c = self.bot.get_channel(589546367605669892)

      emb = discord.Embed(title = "New Feedback", colour = colour, description = feedback, timestamp = ctx.message.created_at)
      emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
      
      msg = await c.send(embed = emb)
      await msg.add_reaction("<a:upvote:639355848031993867>")
      await ctx.send("Done!")

    @commands.command(aliases = ["ae"])
    async def addemoji(self, ctx, name = None, emoji_link = None):

      "Add an emoji"

      if not name:

        name = ctx.author.name

      if not emoji_link:
        
        async with aiohttp.ClientSession() as ses:

          for a in ctx.message.attachments:

            link = a.url
          
          res = await ses.get(link)
          
          img = await res.read()
          
          await ctx.guild.create_custom_emoji(name = name, image = img, reason = f"Emoji added by {ctx.author}")

          await ctx.send("Done!")

      else:
        
        async with aiohttp.ClientSession() as ses:
          
          res = await ses.get(emoji_link)
          
          img = await res.read()
          
          await ctx.guild.create_custom_emoji(name = name, image = img, reason = f"Emoji added by {ctx.author}")

          await ctx.send("Done!")

    @commands.command()
    async def say(self, ctx, *, message):

      "Say something with Satoru"

      if "@everyone" in message:
        
        a = message.replace("@everyone", "everyone")

      elif "@here" in message:

        a = message.replace("@here", "here")
        
      else:
        
        a = message
        
      await ctx.send(a)




def setup(bot):
    bot.add_cog(Misc(bot))