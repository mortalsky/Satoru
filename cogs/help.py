import discord
from discord.ext import commands
import json
import asyncio

colour = 0xbf794b

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True)
    async def help(self, ctx, *, command: str = None):

      with open("data/prefixes.json", "r") as f:

        l = json.load(f)

      try:

        prefix2 = l[str(ctx.guild.id)]

      except KeyError:

        prefix2 = "e?"

      if ctx.prefix == f"<@{self.bot.user.id}> ":
        
        prf = f"@{self.bot.user} "
          
      else:
            
        prf = ctx.prefix

      error = f'```css\nThat command, "{command}", does not exist!\n```'

      res = ""      
      emb = discord.Embed(title = "Help", colour = 0xbf794b)
      emb.set_footer(text = f"Need help about a command? Try {prf}help command")
      
      if command:
        
        cmd = self.bot.get_command(command)

        if not cmd:

          await ctx.send(error)

          return

        if not cmd.hidden:

          if cmd.parent:

            emb.add_field(value = f'{prf}{cmd.parent} {cmd.name} {cmd.signature}', name = cmd.help, inline = False)

          else:
            
            emb.add_field(value = f'{prf}{cmd.name} {cmd.signature}', name = cmd.help, inline = False)
          
          if cmd.aliases:

            aliases = ""

            for a in cmd.aliases:

              aliases += f"\n`{a}`"
            
            emb.add_field(name = 'Aliases', value = aliases, inline = False)

          try:
            
            commands = ""
            
            for a in cmd.commands:
              
              commands += f"`{prf}{cmd.name} {a.name} {a.signature}`\n"
              
            emb.add_field(name = "Subcommands", value = commands, inline = False)

          except:

            pass
        
        else:

          await ctx.send(error)
          return

        await ctx.send(embed = emb)
        await ctx.message.add_reaction("<:greenTick:596576670815879169>")

        return

      for c in self.bot.commands:

        if not c.hidden:

          if ctx.prefix == f"<@!{self.bot.user.id}> ":

            prf = f"@{self.bot.user} "
          
          else:
            
            prf = ctx.prefix

          mod = ""

          for a in self.bot.commands:
            if a.cog_name == "Moderation":
              if not a.hidden:
                mod += f"`{a.name}` :: "

          utility = ""

          for a in self.bot.commands:
            if a.cog_name == "Utility":
              if not a.hidden:

                utility += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    utility += f"`{a.name} {b.name}` :: "

                except:

                  pass

          profiles = ""

          for a in self.bot.commands:
            if a.cog_name == "Profiles":
              if not a.hidden:
                profiles += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    profiles += f"`{a.name} {b.name}` :: "

                except:

                  pass

          misc = ""

          for a in self.bot.commands:
            if a.cog_name == "Misc":
              if not a.hidden:
                misc += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    misc += f"`{a.name} {b.name}` :: "

                except:

                  pass

          weeb = ""

          for a in self.bot.commands:
            if a.cog_name == "Weeb":
              if not a.hidden:
                weeb += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    weeb += f"`{a.name} {b.name}` :: "

                except:

                  pass

          battle = ""

          for a in self.bot.commands:
            if a.cog_name == "Battle":
              if not a.hidden:
                battle += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    battle += f"`{a.name} {b.name}` :: "

                except:

                  pass

          triggers = ""

          for a in self.bot.commands:
            if a.cog_name == "AutoTriggers":
              if not a.hidden:
                triggers += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    triggers += f"`{a.name} {b.name}` :: "

                except:

                  pass

          mc = ""

          for a in self.bot.commands:
            if a.cog_name == "Minecraft":
              if not a.hidden:
                mc += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    mc += f"`{a.name} {b.name}` :: "

                except:

                  pass

          seed = ""

          for a in self.bot.commands:
            if a.cog_name == "SeedCollector":
              if not a.hidden:
                seed += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    seed += f"`{a.name} {b.name}` :: "

                except:

                  pass

          images = ""

          for a in self.bot.commands:
            if a.cog_name == "Images":
              if not a.hidden:
                images += f"`{a.name}` :: "

                try:
                  
                  for b in a.commands:

                    images += f"`{a.name} {b.name}` :: "

                except:

                  pass
          
          res = f"""Server Prefixes: `{prefix2}`, `@{self.bot.user}`

[Support Server](https://discord.gg/w8cbssP)
[Command List](https://satoru.seba.gq/commands)

**MODERATION**
{mod}

**UTILITY**
{utility}

**IMAGES**
{images}

**PROFILE**
{profiles}

**MISC**
{misc}

**WEEB**
{weeb}

**AUTO TRIGGERS**
{triggers}

**MINECRAFT**
{mc}

**SEED COLLECTOR**
{seed}

**BATTLE**
{battle}"""

      emb.description = res

      msg = await ctx.send(embed = emb)

      await ctx.message.add_reaction("<:greenTick:596576670815879169>")

      await msg.add_reaction(str("<:status_dnd:596576774364856321>"))

      def check(reaction, user):

        return user == ctx.author and str(reaction.emoji) == '<:status_dnd:596576774364856321>'

      try:
        
        await self.bot.wait_for("reaction_add", check = check, timeout = 190)
        await msg.delete()

      except asyncio.TimeoutError:

        return 

def setup(bot):
    bot.add_cog(Help(bot))