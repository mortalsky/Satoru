import discord
from discord.ext import commands
import json

colour = 0xbf794b

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases = ["setprefix"], invoke_without_command = True)
    @commands.has_permissions(manage_roles = True)
    async def prefix(self, ctx, *, prefix):

      "Set a custom prefix"

      with open("data/prefixes.json", "r") as f:

        l = json.load(f)

      l[str(ctx.guild.id)] = prefix

      with open("data/prefixes.json", "w") as f:

        json.dump(l, f, indent = 4)

      await ctx.send(f"Prefix for **{ctx.guild.name}** set to `{prefix}`.")

    @prefix.command()
    async def reset(self, ctx):

      "Reset the default prefix"

      with open("data/prefixes.json", "r") as f:

        l = json.load(f)

      try:
        
        l.pop(str(ctx.guild.id))

        with open("data/prefixes.json", "w") as f:

          json.dump(l, f)

        await ctx.send(f"Prefix reset to `e?`.")

      except KeyError:

        await ctx.send("Prefix is already the default one (`e?`).")


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

          booster = f"🎆 | Booster since {member.premium_since.strftime('%m / %d / %Y (%H:%M)')}"

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

          booster = f"🎆 | Booster since {member.premium_since.strftime('%m / %d / %Y (%H:%M)')}"

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

def setup(bot):
    bot.add_cog(Utility(bot))