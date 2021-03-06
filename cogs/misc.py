import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
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
import time
import praw
from dotenv import load_dotenv
import os
from io import BytesIO

load_dotenv(dotenv_path = ".env")

reddit = praw.Reddit(client_id='MBUXLwBBM0mj6A', client_secret = os.getenv("reddit"), user_agent='sebamemes')

translator = Translator()

colour = 0xfffca6

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def hastebin(self, data):
      data = bytes(data, 'utf-8')
      async with aiohttp.ClientSession() as cs:
        async with cs.post('https://hastebin.com/documents', data = data) as r:
          res = await r.json()
          key = res["key"]
          return f"https://hastebin.com/{key}"

    @commands.command()
    async def ping(self, ctx):

      "See bot latency"

      start = time.perf_counter()

      msg = await ctx.send(f"Ping...")

      end = time.perf_counter()
      duration = (end - start) * 1000

      pong = round(self.bot.latency * 1000)

      emb = discord.Embed(colour = discord.Colour.blurple(), description = f"""
```prolog
Latency  :: {pong}ms
Response :: {duration:.2f}ms
```""", timestamp = ctx.message.created_at, title = ":ping_pong: | Pong!")

      await msg.edit(embed = emb, content = None)

    @commands.command(aliases = ["ut"])
    async def uptime(self, ctx):

      "See bot uptime"

      with open("data/stats.json", "r") as f:

        l = json.load(f)

      emb = discord.Embed(description = f':clock: | {l["uptime"]}', colour = colour)

      await ctx.send(embed = emb)

    @commands.command()
    async def meme(self, ctx):
      
      "Get a random meme"

      async with ctx.typing():
        
        emb = discord.Embed(colour = discord.Colour.blurple())
    
        r = random.choice([a for a in reddit.subreddit("dankmemes").hot(limit = 50) if not a.is_self])

        emb.title = r.title
        emb.description = f"<a:upvote:639355848031993867> | {r.ups}"
        emb.url = r.url
        emb.set_image(url = r.url)
        emb.set_footer(text = "r/dankmemes")

      await ctx.send(embed = emb)
    
    @commands.command()
    @commands.is_owner()
    async def reddit(self, ctx, *, subreddit):
      
      "Get a random post from a subreddit"

      async with ctx.typing():
        
        emb = discord.Embed(colour = discord.Colour.blurple())
    
        r = random.choice([a for a in reddit.subreddit(str(subreddit)).hot(limit = 100) if not a.is_self])

        emb.title = r.title
        emb.description = f"<a:upvote:639355848031993867> | {r.ups}"
        emb.url = r.url
        emb.set_image(url = r.url)
        emb.set_author(name = r.author)
        emb.set_footer(text = r.subreddit.display_name)

      await ctx.send(embed = emb)

    async def translate(self, text, source = None, destination = None):
      
      if destination:
        t = translator.translate(text, dest = destination)

      elif source:
        t = translator.translate(text, src = source)

      else:
        t = translator.translate(text)

      return t

    @commands.command(aliases = ["tr"], name = "translate")
    async def translate_(self, ctx, text, source = None, destination = None):

      'Translate a phrase in every language. Use - translate "your text here" first_language second_language - Write languages as en, it, es, fr....'

      t = await self.translate(text, source, destination)

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

    @feedback.error
    async def feedback_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        a = commands.clean_content(use_nicknames = True)
        ctx.prefix = await a.convert(ctx, ctx.prefix)
        emb = discord.Embed(description = f"<:redTick:596576672149667840> | Wrong usage! Use `{ctx.prefix}feedback <your feedback>`.", colour = discord.Colour.red())
        return await ctx.send(embed = emb, delete_after = 10) 

    @commands.command()
    async def say(self, ctx, *, message = None):

      "Say something with Satoru"

      if not message:
        if ctx.message.attachments:
          file = await ctx.message.attachments[0].to_file()
          return await ctx.send(file = file)
        else:
          emb = discord.Embed(description = f"<:redTick:596576672149667840> | Wrong usage! Use `{ctx.prefix}say <your message>`.", colour = discord.Colour.red())
          return await ctx.send(embed = emb, delete_after = 10) 
      if ctx.message.attachments:
        file = await ctx.message.attachments[0].to_file()
      else:
        file = None
      a = commands.clean_content(use_nicknames = True)
      message = await a.convert(ctx, message)

      await ctx.send(message, file = file)

    @say.error
    async def say_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        a = commands.clean_content(use_nicknames = True)
        ctx.prefix = await a.convert(ctx, ctx.prefix)
        emb = discord.Embed(description = f"<:redTick:596576672149667840> | Wrong usage! Use `{ctx.prefix}say <your message>`.", colour = discord.Colour.red())
        return await ctx.send(embed = emb, delete_after = 10) 
      else:
        await ctx.send(error)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def leave(self, ctx, *, member: discord.Member = None):
      "Fake leave the guild"
      member = member or ctx.author
      await ctx.send(f"<:leave:694103681272119346> {member.mention} has left **{ctx.guild.name}**")


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

      "Remove an obj from the list"

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

      invite = discord.utils.oauth_url(self.bot.user.id, permissions = discord.Permissions(permissions = 1074129990))
       
      await ctx.send(f"<{invite}>")

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

      if type in ["second", "seconds", "s", "sec", "secs"]:
        
        await asyncio.sleep(int(time))

        return await ctx.send(content = ctx.author.mention, embed = emb)

      elif type in ["minutes", "min", "mins", "m", "minute"]:

        for a in range(int(time)):

          await asyncio.sleep(60)

        return await ctx.send(content = ctx.author.mention, embed = emb)

      elif type in ["hour", "hours", "h"]:

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

    @commands.command(usage = "[top] [bottom]")
    async def drake(self, ctx, *, text):

      "Make the Drake Meme, use \",\" to separate"

      text = text.split(", ")

      top = text[0]
      bottom = text[1]

      bottom = bottom.replace('"', " ")

      url = f"https://api.alexflipnote.dev/drake?top={top}&bottom={bottom}"

      url = url.replace(" ", "+")

      async with ctx.typing():
        
        async with aiohttp.ClientSession() as cs:
          
          async with cs.get(url) as r:
            
            res = await r.read()
          
        await ctx.send(file = discord.File(io.BytesIO(res), filename="Drake.png"))

      await cs.close()

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
        
        perc = ((100 * int(count))/int(limit))
        
        emb = discord.Embed(description = f"{a} sent **{count} ({perc}%)** messages in {channel.mention} in the last **{limit}** messages.", colour = colour)
        
        await ctx.send(embed = emb)

    @commands.command()
    async def spoiler(self, ctx, *, message):

      "Make a message with a lot of spoilers"

      res = ""

      for a in message:

        res += f"||{a}||"

      await ctx.send(discord.utils.escape_mentions(res))

    async def from_utc(self, timezone):

      local_tz = pytz.timezone(str(timezone))
      
      local_dt = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz)

      return local_tz.normalize(local_dt).strftime("%d %b %Y - %I:%M:%S %p")

    @commands.command(aliases = ["tz", "timezones"])
    async def timezone(self, ctx, *, timezone = None):

      "See what time is in a country"

      if not timezone:

        async with ctx.typing():

          rome = await self.from_utc("Europe/Rome")
          paris = await self.from_utc("Europe/Paris")
          tokyo = await self.from_utc("Asia/Tokyo") 
          london = await self.from_utc("Europe/London")
          berlin = await self.from_utc("Europe/Berlin")
          moscow = await self.from_utc("Europe/Moscow")
          toronto = await self.from_utc("America/Toronto")
          detroit = await self.from_utc("America/Detroit")
          shanghai = await self.from_utc("Asia/Shanghai")
          helsinki = await self.from_utc("Europe/Helsinki")
          newyork = await self.from_utc("America/New_York")
          amsterdam = await self.from_utc("Europe/Amsterdam")

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
      
        emb = discord.Embed(description = f"```prolog\n{timezone} :: {await self.from_utc(str(timezone))}\n```", colour = discord.Colour.blurple())

        await ctx.send(embed = emb)

      except:

        emb = discord.Embed(description = f"**{timezone}** is not a valid timezone!\n\nUse a format like this: **Europe/Rome**.\n\n[Here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) is a list of timezones", colour = discord.Colour.red())

        await ctx.send(embed = emb)

    @commands.command()
    async def poll(self, ctx, poll, *, options = None):

      "Make a poll"

      if not options:

        emb = discord.Embed(title = f"⁉️ | {poll}", colour = discord.Colour.blurple())
        emb.set_footer(text = "Vote")

        msg = await ctx.send(embed = emb)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

        return

      options = options.split(",")

      if len(options) > 10:

        return await ctx.send("Max 10 options!")

      elif len(options) < 2:

        return await ctx.send("Min 2 options!")

      count = 0

      emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

      res = ""

      for a in options:

        emoji = emojis[int(count)]
        count += 1
        res += f"\n{emoji} - {a}"

      emb = discord.Embed(title = f"⁉️ | {poll}", description = res, colour = discord.Colour.blurple())
      emb.set_footer(text = "Vote")

      msg = await ctx.send(embed = emb)

      for a in emojis[:len(options)]:

        await msg.add_reaction(a)

    @commands.command()
    async def clap(self, ctx, *message):
      
      "clap clap"

      clap = " 👏 ".join(message)
      a = commands.clean_content(use_nicknames = True)
      msg = await a.convert(ctx, clap)

      await ctx.send(f"👏 {msg} 👏")

    @commands.command(aliases = ["src", "github"])
    async def source(self, ctx):

      "See Bot source on github"

      await ctx.send("https://github.com/ssebastianoo/Satoru")

    @commands.command()
    async def vote(self, ctx):

      "Vote the bot on top.gg"

      await ctx.send("https://top.gg/bot/635044836830871562/vote")

    @commands.command(aliases = ["spaces"])
    async def space(self, ctx, *, text):

      "Make a lot of spaces between letters"

      a = commands.clean_content(use_nicknames = True)

      msg = await a.convert(ctx, text)

      message = "  ".join(msg)

      await ctx.send(message)

    @commands.command(aliases = ["doggo"])
    async def dog(self, ctx):

      "Get a random dog picture"

      async with aiohttp.ClientSession() as cs:
        
        async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
          
          res = await r.json()  
          
          url = res["message"]

      if ctx.author.nick:

        nick = ctx.author.nick

      else:

        nick = ctx.author.name

      emb = discord.Embed(title = "Doggo", url = url, colour = colour, timestamp = ctx.message.created_at)
      emb.set_author(name = nick, icon_url = ctx.author.avatar_url)
      emb.set_image(url = url)
      
      await ctx.send(embed = emb)

    @commands.command(aliases = ["catto", "pussy"])
    async def cat(self, ctx):

      "Get a random cat picture"

      async with aiohttp.ClientSession() as cs:
        
        async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
          
          res = await r.json()  # returns dict
          
          url = res[0]['url']

      if ctx.author.nick:

        nick = ctx.author.nick

      else:

        nick = ctx.author.name

      emb = discord.Embed(title = "Cat", url = url, colour = colour, timestamp = ctx.message.created_at)
      emb.set_author(name = nick, icon_url = ctx.author.avatar_url)
      emb.set_image(url = url)
      
      await ctx.send(embed = emb)

    @commands.command(hidden = True)
    async def players(self, ctx, *, game):

      "See how many players are playing a game"

      players = len([a for a in ctx.guild.members if a.activity and a.activity.name == game])

      if players == 0:

        return await ctx.send(f"Nobody in {ctx.guild.name} is playing {game}.")

      emb = discord.Embed(description = f"{players} users in {ctx.guild.name} are playing {game}.", colour = colour)

      await ctx.send(embed = emb)

    @commands.command(aliases = ["owo"])
    async def owoify(self, ctx, *, text):
      "OwO"

      text = text.replace(" ", "+")
      text = text.replace("\n", "+")

      a = commands.clean_content(use_nicknames = True)
      text = await a.convert(ctx, text)

      async with aiohttp.ClientSession() as cs:
          r = await cs.get(f"https://nekos.life/api/v2/owoify?text={text}")
          b = await r.json()

      await ctx.send(b["owo"])

      await cs.close()

    @commands.command()
    async def mention(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
      "See who pinged / mentioned a member"
      message = None
      async with ctx.typing():
        member = member or ctx.author
        channel = channel or ctx.channel
        async for a in channel.history(limit=5000):
          if a.id == ctx.message.id:
            pass
          else:
            if member.mention in a.content:
              message = a
              break

        if not message:
          emb = discord.Embed(description = f"<:redTick:596576672149667840> | Last mention is too old or {member.mention} got never mentioned and I can't find it!", colour = discord.Colour.red())
          return await ctx.send(embed = emb, delete_after = 10)

        emb = discord.Embed(description = message.content, timestamp = message.created_at, colour = message.author.colour)
        emb.set_author(name = message.author, icon_url = message.author.avatar_url_as(static_format = "png"))

        await ctx.send(embed = emb)

    @commands.command()
    async def binary(self , ctx, *, text):

      text = discord.utils.escape_markdown(text)

      msg = await ctx.send(f"**Choose:\n- 📝 `Binary` to `Text`.\n- 💻 `Text` to `Binary`.**")
      await msg.add_reaction("📝")
      await msg.add_reaction("💻")

      def check(reaction, user):
        return user.id == ctx.author.id and reaction.message.id == msg.id

      end = False

      while not end:

        try:
          msg_ = await self.bot.wait_for("reaction_add", check = check, timeout = 30)
          
        except asyncio.TimeoutError:
          return await ctx.send(f":clock: | {ctx.author.mention} **Timeout**!", delete_after = 60)
          
        if str(msg_[0]) == "💻":
          text = ' '.join(format(ord(x), 'b') for x in text)
          try:
            emb = discord.Embed(description = text, colour = 0x36393E)
            await ctx.send(embed = emb)
            await msg.delete()
          except:
            text = await self.hastebin(text)
            await ctx.send(f"**{ctx.author.mention} text was too long, I uploaded it here:**\n- {text}")
            await msg.delete()
          end = True
          
        elif str(msg_[0]) == "📝":
          b = text.split()
          try:
            ascii_string = ""
            for a in b:
              oof = int(a, 2)
              ascii_character = chr(oof)
              ascii_string += ascii_character
          except:
            await ctx.send(f"**{ctx.author.mention} I can't encode it, are you sure that it is a Binary code?**", delete_after = 40)
            return await msg.delete()
          try:
            emb = discord.Embed(description = ascii_string, colour = 0x36393E)
            await ctx.send(embed = emb)
            await msg.delete()
          except:
            text = await self.hastebin(text)
            await ctx.send(f"**{ctx.author.mention} text was too long, I uploaded it here:**\n- {text}")
            await msg.delete()
          end = True

        else:
          end = False
          
def setup(bot):
  bot.add_cog(Misc(bot))

