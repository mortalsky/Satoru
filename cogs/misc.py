import discord
from discord.ext import commands
import aiohttp
import json
import random
import asyncio
from googletrans import Translator
import requests

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

    @commands.command(aliases = ["info", "ui"])
    async def userinfo(self, ctx, *, member: discord.Member = None):

      "See a member's info"

      if not member:

        member = ctx.author

        if member.nick:

          nick = f"😄 | {member.nick}"

        else: 

          nick = "~~😄 | No Nickname~~"

        if member.activity:

          act = f"🎮 | {member.activity.name}"

        else: 

          act = "~~🎮 | No Activity~~"

        roles = ""

        if member.premium_since:

          booster = f"🎆 | Booster since {member.premium_since}"

        else:

          booster = "~~🎆 | Not a Booster~~"

        for a in member.roles:

          if a.name == "@everyone":

            roles += "@everyone "

          else:

            roles += f"{a.mention} "

        if member.bot:

          bot = "🤖 | Bot"

        else:

          bot = "~~🤖 | Not a Bot~~"

        emb = discord.Embed(title = member.name, description = f"""😀  | {member.name}

🔢 | {member.discriminator}

🆔 | {member.id}

{nick}

{act}

🤍 | {member.status}

🍰 | Created at {member.created_at.strftime("%m / %d / %Y (%H:%M)")}

➡️ | Joined at {member.joined_at.strftime("%m / %d / %Y (%H:%M)")}

{bot}

{booster}

📜 | {roles}""",colour = member.colour, timestamp = ctx.message.created_at)
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon_url)

        await ctx.send(embed = emb)

      else:

        if member.nick:

          nick = f"😄 | {member.nick}"

        else: 

          nick = "~~😄 | No Nickname~~"

        if member.activity:

          act = f"🎮 | {member.activity.name}"

        else: 

          act = "~~🎮 | No Activity~~"

        roles = ""

        if member.premium_since:

          booster = f"🎆 | Booster since {member.premium_since}"

        else:

          booster = "~~🎆 | Not a Booster~~"

        for a in member.roles:

          if a.name == "@everyone":

            roles += "@everyone "

          else:

            roles += f"{a.mention} "

        if member.bot:

          bot = "🤖 | Bot"

        else:

          bot = "~~🤖 | Not a Bot~~"

        emb = discord.Embed(title = member.name, description = f"""😀  | {member.name}

🔢 | {member.discriminator}

🆔 | {member.id}

{nick}

{act}

🤍 | {member.status}

🍰 | Created at {member.created_at.strftime("%m / %d / %Y (%H:%M)")}

➡️ | Joined at {member.joined_at.strftime("%m / %d / %Y (%H:%M)")}

{bot}

{booster}

📜 | {roles}""",colour = member.colour, timestamp = ctx.message.created_at)
        emb.set_thumbnail(url = member.avatar_url)
        emb.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon_url)

        await ctx.send(embed = emb)

    @commands.command(aliases = ["ri"])
    async def roleinfo(self, ctx, *, role: discord.Role):

      "See a role info"

      if role.hoist:

        hoist = f"📲 | Is Hoist"

      else:

        hoist = f"~~📲 | Isn't Hoist~~"

      if role.managed:

        managed = f"⌨️ | Is Managed"

      else: 

        managed = f"~~⌨️ | Isn't Managed~~"

      if role.mentionable:

        mentionable = f"🏓 | Is Mentionable"
      
      else:

        mentionable = f"~~🏓 | Isn't Mentionable~~"

      if role.is_default():

        default = f"📐 | By Default"

      else:

        default = "~~📐 | Not By Default~~"

      emb = discord.Embed(title = role.name, description = f"""
😀  | {role.name}

🆔 | {role.id}

📢 | {role.mention}

🍰 | Created at {role.created_at.strftime("%m / %d / %Y (%H:%M)")}

🙅 | {len(role.members)} users

📑 | {role.position}° position

🎨 | {role.colour}

🛑 | {role.permissions.value} Perms Value

{hoist}

{managed}

{mentionable}

{default}
""", colour = role.colour, timestamp = ctx.message.created_at)
      emb.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon_url)
      await ctx.send(embed = emb)

    @commands.group(invoke_without_command = True)
    async def list(self, ctx):

      "See your list"

      try:
        
        with open("data/list.json", "r") as f:
          
          l = json.load(f)
          
        res = ""
        
        for a in l[str(ctx.author.id)]:
          
          res += f"{a}\n"

      except KeyError:

        res = ""
          
      emb = discord.Embed(description = res, colour = colour)

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
    async def clear(self, ctx):

      "Clear the list"    

      with open("data/list.json", "r") as f:

        l = json.load(f)

      l.pop(str(ctx.author.id))

      with open("data/list.json", "w") as f:

        json.dump(l, f, indent = 4)

      await ctx.send("Done")

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

    @commands.command(aliases = ["gi"])
    async def guildinfo(self, ctx):

      "See the actual guild info"

      guild = ctx.guild

      if guild.afk_channel:

        afk = f"💤 | {guild.afk_channel}"

      else:

        afk = "~~💤 | No Afk Channel~~"

      roles = ""

      for a in guild.roles:

        if a.name == "@everyone":

          roles += "@everyone "

        else:
          
          roles += f"{a.mention} "

      if not guild.unavailable:

        unav = "🔒 | Is Available"
      
      else: 

        unav = "~~🔒 | Isn't Available~~"

      res = ""

      for a in guild.features:
          
          res += f"{a}, "

      if guild.features:

        features = f"🍔 | {res}"

      else:

        features = "~~🍔 | No Features~~"

      if guild.premium_tier > 0:

        level = f"🎆 | {guild.premium_tier} Nitro Boost Level "

      else:

        level = "~~🎆 | No Booster Level~~"

      if guild.premium_subscription_count > 0:

        boosters = f"💢 | {guild.premium_subscription_count} Boosts"

      else:

        boosters = "~~💢 | No Boosts~~"

      emojis = ""

      for a in guild.emojis:

        emojis += f"{a} "

      online = sum(m.status == discord.Status.online and not m.bot for m in ctx.guild.members)

      dnd = sum(m.status == discord.Status.dnd and not m.bot for m in ctx.guild.members)

      idle = sum(m.status == discord.Status.idle and not m.bot for m in ctx.guild.members)

      offline = sum(m.status == discord.Status.offline and not m.bot for m in ctx.guild.members)

      bots = sum(m.bot for m in ctx.guild.members)
      
      emb = discord.Embed(timestamp = ctx.message.created_at, title = guild.name, description = f"""😀  | {guild.name}

🆔 | {guild.id}

🗺️ | {guild.region}

😴 | {guild.afk_timeout} Seconds

{afk}

👤 | {guild.owner.mention}

🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}

{unav}

👮 | {guild.verification_level} 

{features}

{level}

{boosters}

👥 | {guild.member_count} Members

<:status_online:596576749790429200> | {online} Members

<:status_dnd:596576774364856321> | {dnd} Members

<:status_idle:596576773488115722> | {idle} Members

<:status_offline:596576752013279242> | {offline} Members

🤖 | {bots} Bots

📜 | {roles}""", colour = ctx.author.colour)
      emb.set_thumbnail(url = guild.icon_url)
      emb.set_footer(text = guild.name, icon_url = guild.icon_url)

      if guild.banner:

        emb.set_image(url = guild.banner_url)

      await ctx.send(embed = emb)

    @commands.command()
    async def invite(self, ctx):

       "Invite the bot to your server"
       
       await ctx.send(embed = discord.Embed(description = "[Invite Me](https://discordapp.com/api/oauth2/authorize?client_id=635044836830871562&permissions=321606&scope=bot)", colour = colour))

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):

      "See a member avatar"

      if not member:

        member = ctx.author

      else:

        member = member

      emb = discord.Embed(colour = member.colour, timestamp = ctx.message.created_at)
      emb.set_image(url = member.avatar_url)
      emb.set_footer(text = member.guild.name, icon_url = member.guild.icon_url)
      await ctx.send(embed = emb)

    @commands.command()
    async def about(self, ctx):

      "Info about the bot"

      emb = discord.Embed(description = f"""**Developer: `Sebastiano#5005`
Library: `discord.py 1.2.5`
Python: `3.7.4`
Invite Link: [Click Me](https://discordapp.com/api/oauth2/authorize?client_id=635044836830871562&permissions=321606&scope=bot)
Support Server: [Click Me](https://discord.gg/w8cbssP)
GitHub: [Click Me](https://github.com/ssebastianoo/Satoru)**""", colour = colour)

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

def setup(bot):
    bot.add_cog(Misc(bot))