import discord
import json
from discord.ext import commands
import os
from keep_alive import keep_alive
import asyncio
import requests

bot = commands.Bot(command_prefix = commands.when_mentioned_or('e?'))
bot.remove_command('help')
bot.load_extension('jishaku')

@bot.event
async def on_ready():
  print('Ready as', bot.user)
  await bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.streaming, name = 'e?help', url = 'https://www.twitch.tv/itermosifoni'))

@bot.event 
async def on_message(message):

  await bot.process_commands(message)

  with open('text.txt', 'a') as f:

    f.write(f'{message.author}: {message.content}\n')

  if message.author == bot.user:
      return

  if message.channel.id == 635860414772805642:

    emb = discord.Embed(title = 'New Suggestion', description = message.content, colour = 0xbf794b)
    emb.set_author(name = message.author, icon_url = message.author.avatar_url)
    emb.set_footer(text = 'Erased Bot Suggestion', icon_url = 'https://www.erased.ml/api/satoru/2.png')

    msg = await message.channel.send(embed = emb)
    await message.delete()
    await msg.add_reaction('<a:upvote:635862260085948416>')
    return

  if message.channel.id == 635927405881458768:
    
    if not message.attachments:
      await message.delete()
      return

    for a in message.attachments:

      emb = discord.Embed(title = 'Erased Image', colour = 0xbf794b)
      emb.set_author(name = message.author, icon_url = message.author.avatar_url)
      emb.set_image(url = a.url)
      await message.channel.send(embed = emb)
      await asyncio.sleep(6)
      await message.delete()


@bot.event 
async def on_raw_reaction_add(payload):

  emoji = payload.emoji
  user_id = payload.user_id
  message_id = payload.message_id

  guild = bot.get_guild(635553753344507935)
  member = await guild.fetch_member(user_id)
  updates = discord.utils.get(guild.roles, name = 'Updates')

  if message_id == 635870267658469426:

    if emoji.name == '🏓':
      
      await member.add_roles(updates)
      
@bot.event 
async def on_raw_reaction_remove(payload):

  emoji = payload.emoji
  user_id = payload.user_id
  message_id = payload.message_id

  guild = bot.get_guild(635553753344507935)
  member = await guild.fetch_member(user_id)
  updates = discord.utils.get(guild.roles, name = 'Updates')

  if message_id == 635870267658469426:

    if emoji.name == '🏓':
      
      await member.remove_roles(updates)
      
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
token = os.environ.get('secret')
bot.run(token)