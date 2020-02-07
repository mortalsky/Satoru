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
`{prf}ban` `{prf}kick` `{prf}clear`

**INFO**
`{prf}info` `{prf}roleinfo` `{prf}guildinfo` `{prf}avatar` 

**MISC**
`{prf}ping` `{prf}invite` `{prf}addemoji` `{prf}feedback` `{prf}say` `{prf}looneytunes`

**WEEB**
`{prf}satoru` `{prf}kayo` `{prf}punch` `{prf}hug`"""

      emb.description = res

      await ctx.send(embed = emb)

    @commands.command(hidden = True)
    @commands.is_owner()
    async def test(self, ctx, command: str = None):

      error = f'```css\nThat command, "{command}", does not exist!\n```'

      emb = discord.Embed(title = f'Help for {ctx.author.name}', colour = 0xbf794b)
      emb.set_footer(text = f"Need help about a command? {ctx.prefix.replace(self.bot.user.mention, f'@{self.bot.user.name}#{self.bot.user.discriminator}')}help <command>")
      
      if command:

        cmd = self.bot.get_command(command)

        if not cmd:

          for cog in self.bot.cogs:

            cmd1 = list(int(command).get_commands())

            emb.add_field(name = cmd1.name, value = cmd1.help)

            await ctx.send(embed = emb)

          await ctx.send(error)

          return

        if not cmd.hidden:
          
          emb.add_field(name = f'{ctx.prefix}{cmd.name} {cmd.signature}', value = cmd.help, inline = False)
          
          if cmd.aliases:
            
            emb.add_field(name = 'Aliases', value = cmd.aliases, inline = False)
        
        else:

          await ctx.send(error)
          return


        await ctx.send(embed = emb)
        
        return

      for c in self.bot.commands:

  
        if not c.hidden:
          
          emb.add_field(name = f'<a:dance:637619812989796363> {ctx.prefix}{c.name} {c.signature}', value = f'<a:text:637622070351495169> {c.help}', inline = False)

      await ctx.send(embed = emb)
      
def setup(bot):
    bot.add_cog(Help(bot))