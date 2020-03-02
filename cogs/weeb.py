import discord
from discord.ext import commands 
import random

#COLOUR: 0xbf794b

class Weeb(commands.Cog):

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

  @commands.command(aliases = ['s'])
  async def satoru(self, ctx):

    "See a random image of Satoru Fujinuma"


    satoru = [
      
      'https://cdn.discordapp.com/attachments/567855878808666123/568095828200128542/JPEG_20190417_013431.jpg', 'https://cdn.discordapp.com/attachments/567855878808666123/568095796357103616/JPEG_20190417_161505.jpg', 'https://cdn.discordapp.com/attachments/567855878808666123/568095884529631233/230de8379a4b69316f11d8a192593459.jpg', 'https://cdn.discordapp.com/attachments/567855878808666123/568095884970295326/Satoru_Age_10.png', 'https://cdn.discordapp.com/attachments/567855878808666123/568502695334379530/erased2.jpg', 'https://cdn.discordapp.com/attachments/567855878808666123/568504883435536397/039400c758ce99c4e5c01beec2fd0e43.gif', 'https://cdn.discordapp.com/attachments/567855878808666123/568505242078019585/6139076e42b9a22fc29c49f62a7a2daf.gif', 'https://cdn.discordapp.com/attachments/567855878808666123/568509072886726657/original.gif', 'https://cdn.discordapp.com/attachments/552786907424358401/585555455493931013/gif.gif', 'http://pa1.narvii.com/6049/51fddc4cccaa9e505817276fd493f403869a66ba_hq.gif', 'https://45.media.tumblr.com/f5a0dbd167388edcf846ae0f3272f996/tumblr_o3u3nr5b0H1tndn6wo1_540.gif', 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/09c762af-2eb0-48e5-9585-71db4c1d4b0a/db11gjj-c4065b47-67d3-4c42-a2b0-ab2376a90f06.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzA5Yzc2MmFmLTJlYjAtNDhlNS05NTg1LTcxZGI0YzFkNGIwYVwvZGIxMWdqai1jNDA2NWI0Ny02N2QzLTRjNDItYTJiMC1hYjIzNzZhOTBmMDYuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.OnhQMmif-1fCSezwsO-GWbo4cI18v9mmJclL_cu2hXQ', 'https://i.imgur.com/jWUyzud.gif'

    ]
      
  

    r = random.choice(satoru)

    emb = discord.Embed(description = f'[Satoru!]({r})', colour = 0xbf794b)
    emb.set_image(url = r)

    await ctx.send(embed = emb)

  @commands.command(aliases = ['k'])
  async def kayo(self, ctx):

    "See a random image of Kayo Hinazuki"


    kayo = [
      
      'https://cdn.discordapp.com/attachments/567855878808666123/568502695334379530/erased2.jpg', 'https://cdn.discordapp.com/attachments/567855878808666123/568503526255362052/hinazuki_kayo_12669.jpg', 'https://cdn.discordapp.com/attachments/568107398049300501/568504027688468501/dd24ab7f6464c174de2b5d7d445ef91f.gif', 'https://i.imgur.com/2lmFVRc.gif', 
      'https://fsb.zobj.net/crop.php?r=xjbCHsLWrmxbtwEcG64gnVzInnVCgLw6Mq7JhvEol5SzO-U6xl-BqZrCD4KcAcIK5T8ej8CtOk4U17tQcMMxigbH-DMrmMrMtcLYS2mF5VmfEOTGys7cQ2AemLt63XgmreXcESoq0wuFJ4zOmcO_CkWFjZF2sqAjCTNNeMGfEuBLwBAEpzZ2xYjueu0', 'https://www.bestfunforall.com/cave/imgs/Kayo%20Hinazuki%20Wallpapers%20%2012.jpg', 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/682ca27b-5d49-49ca-8545-7cf9b1324bec/dci2c81-753426d3-7230-4d6f-82a7-0296a3159ff3.jpg/v1/fill/w_770,h_1038,q_70,strp/kayo_hinazuki_by_pwrrakz_dci2c81-pre.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTIxNCIsInBhdGgiOiJcL2ZcLzY4MmNhMjdiLTVkNDktNDljYS04NTQ1LTdjZjliMTMyNGJlY1wvZGNpMmM4MS03NTM0MjZkMy03MjMwLTRkNmYtODJhNy0wMjk2YTMxNTlmZjMuanBnIiwid2lkdGgiOiI8PTkwMCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.y3RmjMpLWe_-aTQLqKGNZcFTIvY7s5yx0nfcXQ7XTa4', 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/9abf104a-edfd-4cca-9ffa-f6844be2d84f/d9t8j0p-d43e4dfc-ac1d-47ba-a9a8-f32c09b69adb.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzlhYmYxMDRhLWVkZmQtNGNjYS05ZmZhLWY2ODQ0YmUyZDg0ZlwvZDl0OGowcC1kNDNlNGRmYy1hYzFkLTQ3YmEtYTlhOC1mMzJjMDliNjlhZGIucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.EIIXWUt3YIM1ADCVDOPnbzNGXLJRMKlVR9vDR36E4W4', 'https://steamuserimages-a.akamaihd.net/ugc/933807958545895899/07CA1F1435BA3CA022E92885CB455AC2623440CD/', 'https://steamuserimages-a.akamaihd.net/ugc/933807761348674982/65647093A3582E294168A612375EB239A61B87B4/', 'https://img.ifunny.co/images/218c63860ae9a6aefca2a6cf3918b19ce84ea896a88df2cfc2f515a34d4cea74_1.gif', 'https://i.pinimg.com/originals/ea/fe/18/eafe18faea2bcf43d465490aceb6ca51.gif'
      
      ]

    r = random.choice(kayo)

    emb = discord.Embed(description = f'[Kayo!]({r})', colour = 0xbf794b)
    emb.set_image(url = r)

    await ctx.send(embed = emb)

def setup(bot):
  bot.add_cog(Weeb(bot))