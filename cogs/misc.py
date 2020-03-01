import discord
from discord.ext import commands
import aiohttp
import json
import random
import asyncio
from googletrans import Translator
from datetime import datetime
import psutil
import platform
import random
import pytz
import traceback

translator = Translator()

colour = 0xbf794b

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):

      "See bot latency"

      pong = round(self.bot.latency * 1000)

      await ctx.send(f":ping_pong: | {pong}ms")

    @commands.command(aliases = ["ut"])
    async def uptime(self, ctx):

      "See bot uptime"

      with open("data/stats.json", "r") as f:
        
        l = json.load(f)

      emb = discord.Embed(description = f':clock: | {l["uptime"]}', colour = colour)

      await ctx.send(embed = emb)

    @commands.command(aliases = ["tr"])
    async def translate(self, ctx, text, source = None, destination = None):

      'Translate a phrase in every language. Use - e?translate "your text here" first_language second_language - Write languages as en, it, es, fr....'

      if destination:
        
        t = translator.translate(text, dest = destination)

      elif source:

        t = translator.translate(text, src = source)

      else:

        t = translator.translate(text)

      if t.dest == "en":

        t.dest = "🇬🇧 | En"

      if t.src == "en":

        t.src = "🇬🇧 | En"

      if t.dest == "es":

        t.dest = "🇪🇸 | Es"

      if t.src == "es":

        t.src = "🇪🇸 | Es"

      if t.src == "it":

        t.src = "🇮🇹 | It"

      if t.dest == "it":

        t.dest = "🇮🇹 | It"

      if t.src == "fr":

        t.src = "🇫🇷 | Fr"

      if t.dest == "fr":

        t.dest = "🇫🇷 | Fr"

      if t.src == "ja":

        t.src = "🇯🇵 | Ja"

      if t.dest == "ja":

        t.dest = "🇯🇵 | Ja"
      
      if t.src == "German":

        t.src == "🇩🇪 | De"


      if t.dest == "German":

        t.dest == "🇩🇪 | De"

      emb = discord.Embed(colour = colour)
      emb.add_field(name = t.src, value = text, inline = False)
      emb.add_field(name = t.dest, value = t.text, inline = False)

      await ctx.send(embed = emb)

    @commands.command(aliases = ["fb"])
    async def feedback(self, ctx, *, feedback):

      "Send a feedback to the bot or suggest a new command"

      c = self.bot.get_channel(589546367605669892)

      emb = discord.Embed(title = "New Feedback", colour = colour, description = feedback, timestamp = ctx.message.created_at)
      emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
      
      msg = await c.send(embed = emb)
      await msg.add_reaction("<a:upvote:639355848031993867>")
      await ctx.send("Done!")

    @commands.command()
    async def say(self, ctx, *, message):

      "Say something with Satoru"

      await ctx.send(discord.utils.escape_mentions(message))

    @commands.group(invoke_without_command = True)
    async def list(self, ctx):

      "See your list"

      try:
        
        with open("data/list.json", "r") as f:
          
          l = json.load(f)

        counter = 0
        res = ""
        
        for a in l[str(ctx.author.id)]:
          
          counter += 1
          res += f"\n{counter} :: {a}"

      except KeyError:

        res = "List is empty"
          
      emb = discord.Embed(description = f"```prolog\n{res}\n```", colour = colour)

      await ctx.send(embed = emb)

    @list.command()
    async def add(self, ctx, *, item):

      "Add something to the list"

      with open("data/list.json", "r") as f:

        l = json.load(f)

      try:
        
        l[str(ctx.author.id)].append(f"{item}")

      except KeyError:

        l[str(ctx.author.id)] = [f"{item}"]

      with open("data/list.json", "w") as f:

        json.dump(l, f, indent = 4)

      await ctx.send("Done!") 

    @list.command()
    async def remove(self, ctx, number_obj: int):

      "Remobe an obj from the list"

      with open("data/list.json", "r") as f:

        l = json.load(f)

      number_obj -= 1

      print(str(ctx.author.id)[int(number_obj)])

      l[str(ctx.author.id)].pop(int(number_obj))

      with open("data/list.json", "w") as f:

        json.dump(l, f, indent = 4)

      await ctx.send("Done!")

    @list.command()
    async def clear(self, ctx):

      "Clear the list"    

      with open("data/list.json", "r") as f:

        l = json.load(f)

      l.pop(str(ctx.author.id))

      with open("data/list.json", "w") as f:

        json.dump(l, f, indent = 4)

      await ctx.send("Done!")

    @commands.command(aliases = ["lt"])
    async def looneytunes(self, ctx):

      "Which Looney Tunes are you?"

      cartoons = [
         "https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Daffy_Duck.svg/1200px-Daffy_Duck.svg.png", "https://upload.wikimedia.org/wikipedia/en/thumb/1/17/Bugs_Bunny.svg/1200px-Bugs_Bunny.svg.png", "https://upload.wikimedia.org/wikipedia/en/thumb/8/88/Porky_Pig.svg/1200px-Porky_Pig.svg.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Elmer_Fudd.png/190px-Elmer_Fudd.png", "https://pngimage.net/wp-content/uploads/2018/06/willy-il-coyote-png-2.png", "https://www.ilnapolista.it/wp-content/uploads/2017/01/beep_beep.png", "https://it.wikifur.com/w/images/thumb/7/70/Gattosilvestro.png/499px-Gattosilvestro.png", "https://cronacheletterarie.com/wp-content/uploads/2012/11/Tweety.png", "https://i.pinimg.com/originals/30/ba/b6/30bab6015b879437e1ec3054f7019c00.png"
      ]

      r = random.choice(cartoons)

      emb1 = discord.Embed(title = f"{ctx.author.name}, which Looney Tunes are you?", colour = colour)
      emb2 = discord.Embed(title = f"{ctx.author.name}, which Looney Tunes are you?", colour = colour)
      emb2.set_image(url = r)

      msg = await ctx.send(embed = emb1)
      await asyncio.sleep(1)
      await msg.edit(embed= emb2)

    @commands.command()
    async def invite(self, ctx):

       "Invite the bot to your server"
       
       await ctx.send(embed = discord.Embed(description = "[Invite Me](https://satoru.seba.gq/invite)", colour = colour))

    @commands.command(aliases = ["stats"])
    async def about(self, ctx):

      "Info about the bot"

      with open("data/stats.json", "r") as f:

        l = json.load(f)

      emb = discord.Embed(description = f"""**Developer: `Sebastiano#3151`
Library: `discord.py {discord.__version__}`
Python: `{platform.python_version()}`
Memory: `{psutil.virtual_memory()[2]}%`
CPU: `{psutil.cpu_percent()}%`
Uptime: `{l["uptime"]}`
Running on: `{platform.system()}`
Guilds: `{len(self.bot.guilds)}`
Users: `{len(self.bot.users)}`
Invite Link: [Click Me](https://satoru.seba.gq/invite)
Website: [Click Me](https://satoru.seba.gq/)
Support Server: [Click Me](https://discord.gg/w8cbssP)
GitHub: [Click Me](https://github.com/ssebastianoo/Satoru)
Top.gg: [Click Me](https://top.gg/bot/635044836830871562)
Vote me: [Click Me](https://top.gg/bot/635044836830871562/vote)
**""", colour = colour)

      await ctx.send(embed = emb)

    @commands.command()
    async def male(self, ctx, thing, member: discord.Member = None):

      "Use this when someone says that a thing is a female but is a male"

      if member:

        res = f"Damnit {member.mention}<:bahrooscreaming:676018783332073472>! {thing} is a **male**!"

      else:

        res = f"Damnit<:bahrooscreaming:676018783332073472>! {thing} is a **male**!"

      emb = discord.Embed(description = res, colour = discord.Colour.red())

      await ctx.send(embed = emb)

    @commands.command()
    async def female(self, ctx, thing, member: discord.Member = None):

      "Use this when someone says that a thing is a male but is a female"


      if member:

        res = f"Damnit {member.mention}<:bahrooscreaming:676018783332073472>! {thing} is a **female**!"

      else:

        res = f"Damnit<:bahrooscreaming:676018783332073472>! {thing} is a **female**!"

      emb = discord.Embed(description = res, colour = discord.Colour.red())

      await ctx.send(embed = emb)

    @commands.command(aliases = ["himym"], hidden = True)
    async def howimetyourmother(self, ctx, season, episode: int):

      "How I Met Your Mother episodes stats"

      episode -= 1

      if season:

        if episode:
          
          async with aiohttp.ClientSession() as cs:
            
            async with cs.get('http://epguides.frecar.no/show/howimetyourmother/') as r:
              
              r = await r.json()  

          await ctx.send(f'''Title: {r[season][episode]["title"]}
Season: {r[season][episode]["season"]}
Episode: {r[season][episode]["number"]}
Release Date: {r[season][episode]["release_date"]}
''')

    @commands.command(name = "random")
    async def _random(self, ctx, *elements):

      "Make a random choice"

      emb = discord.Embed(description = random.choice(elements), colour = colour)

      await ctx.send(embed = emb)

    @commands.command(hidden = True)
    async def remind(self, ctx, time, type, *, what = None):

      "Set an alarm"

      emb = discord.Embed(title = f":clock: | Reminder", description = f"At {ctx.message.created_at.strftime('%d %B %Y [%I:%M %p] UTC')}:\n\n{what}\n\n[Jump]({ctx.message.jump_url})", colour = discord.Colour.dark_teal())

      await ctx.send("Ok!")

      if type == "seconds" or "second" or "sec" or "secs" or "s":
        
        await asyncio.sleep(int(time))

        return await ctx.send(content = ctx.author.mention, embed = emb)

      elif type == "minutes":

        for a in range(int(time)):

          await asyncio.sleep(60)

        return await ctx.send(content = ctx.author.mention, embed = emb)

      elif type == "hours" or "hour" or "h":

        for a in range(int(time)):

          await asyncio.sleep(3600)

        return await ctx.send(content = ctx.author.mention, embed = emb)

    @commands.command(aliases = ["cb"])
    async def codeblock(self, ctx, language, *, code):

      "Transform a code to a codeblock"

      if language == "raw":

        await ctx.send(discord.utils.escape_markdown(f"""```{code}```"""))

      else:
        
        await ctx.send(f"""```{language}\n{code}```""")

    @commands.command()
    async def drake(self, ctx, top, *, bottom):

      "Make the Drake Meme"

      bottom = bottom.replace('"', " ")

      url = f"https://api.alexflipnote.dev/drake?top={top}&bottom={bottom}"

      emb = discord.Embed(colour = discord.Colour.dark_gold())

      emb.set_image(url = url.replace(" ", "+"))

      await ctx.send(embed = emb)

    @commands.command(name = "8ball", aliases = ["8b"])
    async def _8ball(self, ctx, *, question):

      "Ask 8ball a question"

      messages = [
        "Sure!",
        "Obvious!",
        "Hell no!",
        "Stars say: \"Dude what the frick, no!\"."
        "Stars say: \"Oh yes dude!\"."
        "Haha, no."
      ]

      emb = discord.Embed(title = question, description = random.choice(messages), colour = colour, timestamp = ctx.message.created_at)
      emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url_as(static_format = "png"))

      await ctx.send(embed = emb)

    @commands.command()
    async def raw(self, ctx, *, message):

      "Show a message without markdown"

      try:
        
        message = ((await self.bot.get_channel(ctx.channel.id).fetch_message(message)).content)

      except:

        message = message
        
      message = discord.utils.escape_mentions(message)
      a = commands.clean_content(fix_channel_mentions = True, escape_markdown = True)
      message0 = await a.convert(ctx, message)
      message1 = discord.utils.escape_markdown(message0)

      emb = discord.Embed(colour = colour)
      emb.add_field(name = "Raw", value = message0, inline = False)
      emb.add_field(name = "Escape Markdown", value = message1, inline = False)

      await ctx.send(embed = emb)

    @commands.command()
    async def messages(self, ctx, limit = 500, channel: discord.TextChannel = None, member: discord.Member = None):

      """See how many messages a member sent in a channel in the last tot messages
Use `messages <limit> <channel> <member>`"""

      if limit > 5000:

        limit = 5000

      if not channel:

        channel = ctx.channel

      if not member:

        member = ctx.author
        
        a = "You"

      else:

        member = member
        a = member.mention

      async with ctx.typing():
        
        messages = await channel.history(limit=limit).flatten()
        count = len([x for x in messages if x.author.id == member.id])
        
        emb = discord.Embed(description = f"{a} sent **{count}** messages in {channel.mention} in the last **{limit}** messages.", colour = colour)
        
        await ctx.send(embed = emb)

    @commands.command()
    async def spoiler(self, ctx, *, message):

      "Make a message with a lot of spoilers"

      res = ""

      for a in message:

        res += f"||{a}||"

      await ctx.send(discord.utils.escape_mentions(res))

    def from_utc(self, timezone):

      local_tz = pytz.timezone(str(timezone))
      
      local_dt = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz)

      return local_tz.normalize(local_dt).strftime("%d %b %Y - %I:%M:%S %p")

    @commands.command(aliases = ["tz", "timezones"])
    async def timezone(self, ctx, *, timezone = None):

      "See what time is in a country"

      if not timezone:

        async with ctx.typing():

          rome = self.from_utc("Europe/Rome")
          paris = self.from_utc("Europe/Paris")
          tokyo = self.from_utc("Asia/Tokyo") 
          london = self.from_utc("Europe/London")
          berlin = self.from_utc("Europe/Berlin")
          moscow = self.from_utc("Europe/Moscow")
          toronto = self.from_utc("America/Toronto")
          detroit = self.from_utc("America/Detroit")
          shanghai = self.from_utc("Asia/Shanghai")
          helsinki = self.from_utc("Europe/Helsinki")
          newyork = self.from_utc("America/New_York")
          amsterdam = self.from_utc("Europe/Amsterdam")

          emb = discord.Embed(description = f"""```prolog
Rome       ::   {rome}
Paris      ::   {paris}
Tokyo      ::   {tokyo}
London     ::   {london}
Berlin     ::   {berlin}
Moscow     ::   {moscow}
Toronto    ::   {toronto}
Detroit    ::   {detroit}
Shanghai   ::   {shanghai}
Helsinki   ::   {helsinki}
New York   ::   {newyork}
Amsterdam  ::   {amsterdam}
```""", colour = discord.Colour.blurple())

        return await ctx.send(embed = emb)

      try:
      
        emb = discord.Embed(description = f"```prolog\n{timezone} :: {self.from_utc(str(timezone))}\n```", colour = discord.Colour.blurple())

        await ctx.send(embed = emb)

      except:

        emb = discord.Embed(description = f"**{timezone}** is not a valid timezone!\n\nUse a format like this: **Europe/Rome**.\n\n[Here](https://timezonedb.com/time-zones) is a list of timezones", colour = discord.Colour.red())

        await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(Misc(bot))