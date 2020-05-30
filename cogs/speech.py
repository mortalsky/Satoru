import speech_recognition as sr 
import discord
from discord.ext import commands
from io import BytesIO
import aiohttp
import traceback
from gtts import gTTS

r = sr.Recognizer()

class Speech(commands.Cog):
  def __init__(self, bot):
    self.bot = bot 

  async def to_bytes(self, url):
    async with aiohttp.ClientSession() as cs:
      async with cs.get(url) as r:
        res = await r.read() 
        return res

  async def to_text(self, file):
    with sr.AudioFile(file) as source:
      audio = r.record(source)
    try:
      text = r.recognize_google(audio)
      return text
    except:
      return "<:redTick:596576672149667840> | I didn't get it."

  async def tts(self, message):
    tts = gTTS(text=message, lang='en')
    tts.save("tts.mp3")

  @commands.command()
  async def speech(self, ctx):
    "Recognize a voice and make it text"
    try:
      if ctx.message.attachments:

        if ctx.message.attachments[0].filename.endswith(".wav") or ctx.message.attachments[0].filename.endswith(".mp3"):
          b = BytesIO()
          oof = await ctx.message.attachments[0].save(b)
          b.seek(0)
          text = await self.to_text(b)
          emb = discord.Embed(description = text, colour = 0x36393E)
          return await ctx.send(embed = emb)

        else:
          return await ctx.send("Only `.wav` file or `.mp3`.")
      else:
        return await ctx.send("Pls include an audio file")
    except Exception:
      traceback.print_exc()

  @commands.command(aliases = ["tts"])
  async def text_to_speech(self, ctx, *, message):
    "Transform a text to a speech!"
    await self.tts(message)
    f = discord.File("tts.mp3")
    await ctx.send(file = f)

def setup(bot):
  bot.add_cog(Speech(bot))