import discord
from discord.ext import commands 
import random

#COLOUR: 0xbf794b

class Actions(commands.Cog):

  """Make actions with the Erased people"""

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def hug(self, ctx, member: discord.Member = None):
    """Hug a user"""

    hug = [
      'https://media1.tenor.com/images/3c5c8c58f71c8443fd97487cf3c79fae/tenor.gif?itemid=5178498', 'https://i.pinimg.com/originals/11/3c/9c/113c9c00893d75c115cf6a7aab754e06.gif', "https://cdn.nekos.life/hug/hug_034.gif", "https://media3.giphy.com/media/143v0Z4767T15e/giphy.gif", "https://nimg.taadd.com/article/201709/1/1000004_150433331317721.gif", "https://i.kym-cdn.com/photos/images/original/000/935/627/3a5.gif", "https://gifimage.net/wp-content/uploads/2017/09/anime-hug-kiss-gif.gif", "https://media1.giphy.com/media/qscdhWs5o3yb6/giphy.gif", "https://media1.giphy.com/media/yziFo5qYAOgY8/giphy.gif", "https://data.whicdn.com/images/135392484/original.gif", "https://i.pinimg.com/originals/08/de/7a/08de7ad3dcac4e10d27b2c203841a99f.gif", "https://gifimage.net/wp-content/uploads/2018/10/anime-hug-cry-gif.gif", "https://media.indiedb.com/images/groups/1/25/24269/ezgif.com-624b1ca218.gif", "https://images-ext-1.discordapp.net/external/wwKXAwjVHOpM65WE-urMHLfbsi8wcu-QeINmkVUeVJs/https/cdn.ram.moe/B1BzEkMql.gif", "https://i.imgur.com/FCXa6Gx.gif", "https://i.pinimg.com/originals/7f/76/10/7f76102bedf6de4e34065709d16a9ef8.gif", "https://media1.tenor.com/images/d0ce45027c5b5612600ceb8166b2bfe1/tenor.gif?itemid=5226254"
    ]

    r = random.choice(hug)

    if member == ctx.author:

      await ctx.send('It looks like you love yourself...')
      return

    if member == self.bot.user:
      await ctx.send('I love you too:heart:')
      return

    emb = discord.Embed(title = 'Hug!', description = f'{ctx.author.mention} [hugged]({r}) {member.mention}', colour = 0xbf794b)
    emb.set_image(url = r)
    await ctx.send(embed = emb)

  @commands.command()
  async def punch(self, ctx, member: discord.Member = None):
    """Punch a user"""

    punch = [
      'https://media.discordapp.net/attachments/578551279484403733/669202660808720394/iu.png', 'https://pa1.narvii.com/6399/0479c54c73fa33b332c406d20672a688045ff43a_hq.gif', 'https://thumbs.gfycat.com/BeautifulGregariousHare-poster.jpg', "https://pa1.narvii.com/6084/9a9d4e2b8311b4b7428e9fbeea4ae6b45ef265b8_hq.gif", "https://media1.tenor.com/images/6834932465e2659dc5b1ee38dfd42b44/tenor.gif?itemid=14615839", "https://steamuserimages-a.akamaihd.net/ugc/45369364714448191/6E8C6F0D885EC0AD090B81FC599D5B0495F02591/", "https://qph.fs.quoracdn.net/main-qimg-024b359517a272d10b26f703c37e5c28", "https://i.kym-cdn.com/photos/images/original/001/619/890/10b.gif", "https://thumbs.gfycat.com/TeemingMeekGrouse-small.gif"
    ]

    r = random.choice(punch)

    if member == ctx.author:

      await ctx.send('It looks like you like to punch yourself...')
      return

    if member == self.bot.user:
      await ctx.send('Don\'t punch me baka🤬!')
      return

    emb = discord.Embed(title = 'Punch!', description = f'{ctx.author.mention} [punched]({r}) {member.mention}', colour = 0xbf794b)
    emb.set_image(url = r)
    await ctx.send(embed = emb)

def setup(bot):
  bot.add_cog(Actions(bot))