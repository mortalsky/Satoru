from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageOps
import discord
from discord.ext import commands
import aiohttp
import traceback

class Images(commands.Cog):

  def __init__(self, bot):
    self.bot = bot 

  @commands.command(aliases = ["cmm", "mind", "change me"])
  async def change_my_mind(self, ctx, *, text):

    "Change my mind meme"

    async with ctx.typing():

      async with aiohttp.ClientSession() as cs:
          async with cs.get(str(ctx.author.avatar_url_as(format = "png"))) as r:
              res = await r.read()  
      
      base = Image.open('assets/mind.png')
      img = Image.open(BytesIO(res)).resize((100, 100)).convert('RGBA').rotate(30)
      f = ImageFont.truetype('assets/Arial.ttf', 50)
      base.paste(img, (255, 6), img)

      # ---
      # d = ImageDraw.Draw(base)
      # d.text((400,300), str(text), fill=(0,0,0), font = f)
      # ---

      try:

        txt=Image.new('L', (500,500))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), text,  font=f, fill = 255)
        w=txt.rotate(20,  expand=1)

        base.paste(ImageOps.colorize(w, (0,0,0), (0,0,0)), (380,100),  w)

      except Exception:
        traceback.print_exc()

      base = base.convert('RGBA')
      b = BytesIO() 
      base.save(b, "png") 
      b.seek(0)
      await ctx.send(file = discord.File(fp=b, filename = f"Change {ctx.author.display_name}'s mind.png"))

      await cs.close()

  @commands.command()
  async def punch(self, ctx, *, member: discord.Member = None):

    "Punch someone"

    if not member:
      member = ctx.author

    if member == self.bot.user:
      return await ctx.send("no u")

    async with ctx.typing():

      async with aiohttp.ClientSession() as cs1:
          async with cs1.get(str(ctx.author.avatar_url_as(format = "png"))) as r:
              res2 = await r.read()  

      async with aiohttp.ClientSession() as cs2:
          async with cs2.get(str(member.avatar_url_as(format = "png"))) as r:
              res1 = await r.read()  

      base = Image.open('assets/punch.png').convert("RGBA")
      img1 = Image.open(BytesIO(res1)).resize((210, 210)).convert("RGBA")
      img2 = Image.open(BytesIO(res2)).resize((300, 300)).convert("RGBA")
      base.paste(img1, (40, 35), img1)
      base.paste(img2, (480, 30), img2)
      b = BytesIO() 
      base.save(b, "png")
      b.seek(0)
      await ctx.send(file = discord.File(fp=b, filename = "punch.png"))

      await cs1.close()
      await cs2.close()

  @commands.command()
  async def mike(self, ctx, member: discord.Member = None):

    "Mike Bruhzowski"

    if not member: 
      member = ctx.author

    async with ctx.typing():

      async with aiohttp.ClientSession() as cs:
          async with cs.get(str(member.avatar_url_as(format = "png"))) as r:
              res = await r.read()  

      img = Image.open(BytesIO(res)).resize((500, 500))
      img.putalpha(100)
      base = Image.open('assets/mike.png').resize((500, 500))
      base.paste(img, (0, 0), img)
      b = BytesIO()
      base.save(b, "png")
      b.seek(0)
      await ctx.send(file = discord.File(fp = b, filename = "mike.png"))

      await cs.close()

def setup(bot):
  bot.add_cog(Images(bot))