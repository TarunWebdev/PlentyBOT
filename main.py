from pytezos import pytezos


import os
from discord.ext import commands
from mee6_py_api import API
import discord
import random

pytezos = pytezos.using(key="2.json")
pytezos.activate_account()
builder = pytezos.contract('KT1B8HUxpgyUgd73dic6nmoionDd5JBaJKXV')


bot = commands.Bot(command_prefix='!')
mee6API = API("937383693100658689")

@bot.event
async def on_ready():
   print('Logged in as')
   print(bot.user.name)
    

@bot.command(name='mint', help='mint help.')
async def mint(ctx,  arg):
    level = await mee6API.levels.get_user_level(ctx.author.id)
    if level < 10:
      print("no mint")
      opg = pytezos.bulk(
        builder.mintNFT(address=arg , discord=ctx.author.id ),
      ).autofill().sign().inject(_async=False)
    elif level >= 10 and level < 20:
      print("level 10 mint")
    elif level >= 20 and level < 30:
      print("level 20 mint")
    elif level >= 30 and level < 40:
      print("level 30 mint")
    elif level >= 40 and level < 50:
      print("level 40 mint")
    else:
      print("level 50 mint")
    await ctx.channel.send(arg)
    await ctx.channel.send(str(ctx.author.id))
    



@bot.command(name='lvl', help='lvl help.')
async def lvl(ctx):
    #leaderboard
    # leaderboard_page = await mee6API.levels.get_leaderboard_page(0)
    # await ctx.channel.send(leaderboard_page)

    #details
    # details = await mee6API.levels.get_user_details(user_id)
    # print(details)

    #level
    await ctx.channel.send(ctx.author.id)    
    level = await mee6API.levels.get_user_level(ctx.author.id)
    await ctx.channel.send(level)



# my_secret = os.environ['new_token']
bot.run("OTM3MzgzNzQ0NTg5OTUwOTk4.Yfa8pA.qUWJ_ioULzkCqirqkNeFYv0aTX0")

# my_secret = os.environ['token']
