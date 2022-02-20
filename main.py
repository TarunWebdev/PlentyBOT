from pytezos import pytezos
from discord.ext import commands
from mee6_py_api import API
import discord
import re

finderr = re.compile("'with': {'string':(.+')}")

pytezos = pytezos.using(key="2.json")
pytezos.activate_account()
builder = pytezos.contract('KT1RPeo9eQ4inwmvPC6Ma3SWVe3rGeBuc4S4')


bot = commands.Bot(command_prefix='!')
mee6API = API("937383693100658689")

@bot.event
async def on_ready():
   print('Logged in as')
   print(bot.user.name)
    
@bot.command(name='displayembed')
async def displayembed(ctx):
  embed=discord.Embed(title="Pleanty NFT BOT", description="Welcome to Plenty NFT BOT! You have been of great value to our server, to appreciate your participation and want to reward you with a free NFT! Tap the button below to claim.", color=0x00ff33)
  embed.add_field(name="Minimum Level Requirement", value="Level 10", inline=True)
  embed.set_footer(text="Type !mint < Your tezos  wallet adderss >")
  await ctx.send(embed=embed)

@bot.command(name='mint', help='mint help.')
async def mint(ctx,  arg):
    level = await mee6API.levels.get_user_level(ctx.author.id)
    if level < 10:
      print("You do not meet the min req for a mint")
      await ctx.channel.send("You do not meet the min req for a mint")
    elif level >= 10 and level < 20:
      print("level 10 mint")
      try:
        opg = pytezos.bulk(
                builder.mintNFT(address=arg , discord=str(ctx.author.id) ),
              ).autofill().sign().inject(_async=False)
        await ctx.channel.send("Mint Successful, check your Wallet")
      except Exception as e:
        if(finderr.findall(str(e))):
          print(finderr.findall(str(e))[0])
        else:
          print("unknown error: "+ str(e))
    elif level >= 15 and level < 20:
      print("level 15 mint")
      try:
        opg = pytezos.bulk(
                builder.mintNFT(address=arg , discord=str(ctx.author.id) ),
              ).autofill().sign().inject(_async=False)
        await ctx.channel.send("Mint Successful, check your Wallet")
      except Exception as e:
        if(finderr.findall(str(e))):
          print(finderr.findall(str(e))[0])
        else:
          print("unknown error: "+ str(e))
    elif level >= 20 and level < 25:
      print("level 20 mint")
      try:
        opg = pytezos.bulk(
                builder.mintNFT(address=arg , discord=str(ctx.author.id) ),
              ).autofill().sign().inject(_async=False)
        await ctx.channel.send("Mint Successful, check your Wallet")
      except Exception as e:
        if(finderr.findall(str(e))):
          print(finderr.findall(str(e))[0])
        else:
          print("unknown error: "+ str(e))
    elif level >= 25 and level < 30:
      print("level 25 mint")
      try:
        opg = pytezos.bulk(
                builder.mintNFT(address=arg , discord=str(ctx.author.id) ),
              ).autofill().sign().inject(_async=False)
        await ctx.channel.send("Mint Successful, check your Wallet")
      except Exception as e:
        if(finderr.findall(str(e))):
          print(finderr.findall(str(e))[0])
        else:
          print("unknown error: "+ str(e))
    elif level>=30:
      print("level 30 mint")
      try:
        opg = pytezos.bulk(
                builder.mintNFT(address=arg , discord=str(ctx.author.id) ),
              ).autofill().sign().inject(_async=False)
        await ctx.channel.send("Mint Successful, check your Wallet")
      except Exception as e:
        if(finderr.findall(str(e))):
          print(finderr.findall(str(e))[0])
        else:
          print("unknown error: "+ str(e))

    
@bot.command(name='lvl', help='lvl help.')
async def lvl(ctx):
    await ctx.channel.send(ctx.author.id)    
    level = await mee6API.levels.get_user_level(ctx.author.id)
    await ctx.channel.send(level)

bot.run("")

