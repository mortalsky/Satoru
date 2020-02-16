import discord
from discord.ext import commands

#colour = 0xbf794b

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      
      commands = ""

      for a in self.bot.commands:

        if not a.hidden:

          if a.name != "jishaku":
            
            commands += f"`e?{a.name} {a.signature}`\n\n> {a.help} \n\n"
    
      with open("README.md", "w") as f:
      
        f.write(f"""# Satoru
Satoru is a Discord Bot made with discord.py
- Moderation
- Info 
- Misc

**[Invite the bot](https://discordapp.com/api/oauth2/authorize?client_id=635044836830871562&permissions=321606&scope=bot)**

# Commands

{commands}""")


    @commands.command(hidden = True)
    async def help(self, ctx, *, command: str = None):

      error = f'```css\nThat command, "{command}", does not exist!\n```'

      if ctx.prefix == f"<@!635044836830871562> ":

        prefix = f'@{self.bot.user} '
      
      else:

        prefix = ctx.prefix

      res = ""      
      emb = discord.Embed(title = "Help", colour = 0xbf794b)
      emb.set_footer(text = f"Need help about a command? try {prefix}help command")
      

      if command:
        
        cmd = self.bot.get_command(command)

        if not cmd:

          await ctx.send(error)

          return

        if not cmd.hidden:

          if cmd.parent:

            emb.add_field(value = f'{prefix}{cmd.parent} {cmd.name} {cmd.signature}', name = cmd.help, inline = False)

          else:
            
            emb.add_field(value = f'{prefix}{cmd.name} {cmd.signature}', name = cmd.help, inline = False)
          
          if cmd.aliases:

            aliases = ""

            for a in cmd.aliases:

              aliases += f"\n`{a}`"
            
            emb.add_field(name = 'Aliases', value = aliases, inline = False)

          try:
            
            commands = ""
            
            for a in cmd.commands:
              
              commands += f"`{prefix}{cmd.name} {a.name} {a.signature}`\n"
              
            emb.add_field(name = "Subcommands", value = commands, inline = False)

          except:

            pass
        
        else:

          await ctx.send(error)
          return

        await ctx.send(embed = emb)
        
        return

      for c in self.bot.commands:

        if not c.hidden:

          if ctx.prefix == f"<@!{self.bot.user.id}> ":

            prf = f"@{self.bot.user} "
          
          else:
            
            prf = ctx.prefix
          
          res = f"""Prefixes: `e?`, `@{self.bot.user}`

[Support Server](https://discord.gg/w8cbssP)
[Command List](https://satoru.seba.gq/commands)

**MODERATION**
`{prf}ban` `{prf}kick` `{prf}mute` `{prf}unmute` `{prf}clear`

**INFO**
`{prf}userinfo` `{prf}roleinfo` `{prf}guildinfo` `{prf}avatar` 

**MISC**
`{prf}ping` `{prf}invite` `{prf}addemoji` `{prf}feedback` `{prf}say` `{prf}looneytunes` `{prf}uptime` `{prf}about` `{prf}translate` `{prf}gun` `{prf}male` `{prf}female` `{prf}list` `{prf}list add` `{prf}list clear` `{prf}profile` `{prf}profile create` `{prf}delete` `{prf}profile description` `{prf}profile image`    

**WEEB**
`{prf}satoru` `{prf}kayo` `{prf}punch` `{prf}hug`"""

      emb.description = res

      await ctx.send(embed = emb)

    @commands.command(hidden = True, aliases = ["cmd", "cmds", "command"])
    async def commands(self, ctx):

      "See all commands"

      count = 0

      pag = commands.Paginator(prefix = f"```\n", suffix = "\n```", max_size = 50)

      for a in self.bot.commands:

        if not a.hidden:
          
          pag.add_line(f"{a.name} {a.signature}")

      msg = await ctx.send(f"Page number {count}/{len(pag.pages)}\n{pag.pages[0]}")

      await msg.add_reaction("◀️")
      await msg.add_reaction("▶️")
      await msg.add_reaction("⏹️")

      def check(reaction, user):
        
        return user == ctx.author 

      end = False

      while not end:
        
        reaction, user = await self.bot.wait_for('reaction_add', check = check)
          
        if str(reaction.emoji) == "▶️":
          
            count += 1

            if count == 1:
              
              await msg.edit(content = f"Page number {count}/{len(pag.pages)}\n{pag.pages[1]}")

            elif count == 2:

              await msg.edit(content = f"Page number {count}/{len(pag.pages)}\n{pag.pages[1]}")
            
            else:

              if count > len(pag.pages):

                count = 0
              
              else:

                count = count

              await msg.edit(content = f"Page number {count}/{len(pag.pages)}\n{pag.pages[count]}")

        elif str(reaction.emoji) == "◀️":

            count -= 1

            if count == 1:
              
              await msg.edit(content = f"Page number {count}\n{pag.pages[1]}")

            elif count == 2:

              await msg.edit(content = f"Page number {count}\n{pag.pages[2]}")

            elif count == 0:

              await msg.edit(content = f"Page number {count}\n{pag.pages[0]}")
            
            else:

              count = 0

              await msg.edit(content = f"Page number {count}\n{pag.pages[0]}")

        elif str(reaction.emoji) == "⏹️":
 
            end = True

      
def setup(bot):
    bot.add_cog(Help(bot))