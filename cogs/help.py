import discord
from discord.ext import commands

#colour = 0xbf794b

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
          
          emb.add_field(name = f'{prefix}{cmd.name} {cmd.signature}', value = cmd.help, inline = False)
          
          if cmd.aliases:

            aliases = " ".join(cmd.aliases)
            
            emb.add_field(name = 'Aliases', value = aliases, inline = False)
        
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

**MODERATION**
`{prf}ban` `{prf}kick` `{prf}mute` `{prf}unmute` `{prf}clear`

**INFO**
`{prf}info` `{prf}roleinfo` `{prf}guildinfo` `{prf}avatar` 

**MISC**
`{prf}ping` `{prf}invite` `{prf}addemoji` `{prf}feedback` `{prf}say` `{prf}looneytunes` `{prf}uptime` `{prf}about` `{prf}translate` `{prf}gun` `{prf}male` `{prf}female` 

**WEEB**
`{prf}satoru` `{prf}kayo` `{prf}punch` `{prf}hug`"""

      emb.description = res

      await ctx.send(embed = emb)

    @commands.command(hidden = True, aliases = ["cmd"])
    async def commands(self, ctx):

      "See all commands"

      count = 0

      pag = commands.Paginator(prefix = f"```\n", suffix = "\n```", max_size = 500)

      for a in self.bot.commands:

        if not a.hidden:
          
          pag.add_line(f"{a.name} {a.signature}")

      msg = await ctx.send(f"Page number {count}\n{pag.pages[count]}")

      await msg.add_reaction("◀️")
      await msg.add_reaction("▶️")
      await msg.add_reaction("⏹️")

      def check(reaction, user):
        
        return user == ctx.author 

      end = False

      while not end:
        
        reaction, user = await self.bot.wait_for('reaction_add', check = check)

        try:
          
          if str(reaction.emoji) == "▶️":
          
            count += 1
          
            await msg.edit(content = f"Pages number {count}\n{pag.pages[count]}")

          elif str(reaction.emoji) == "◀️":

            count -= 1

            if count < 0:

              count = 0

            await msg.edit(content = f"Page number {count}\n{pag.pages[count]}")

          elif str(reaction.emoji) == "⏹️":
 
            end = True

        except:

          pass
      
def setup(bot):
    bot.add_cog(Help(bot))