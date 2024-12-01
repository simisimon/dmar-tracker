import os
import discord
import requests
import helperFunctions

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#intents = discord.Intents.default()
#intents.typing = False
#intents.presences = False

bot_intents = discord.Intents.all()
#bot_intents.messages = True

bot = commands.Bot(command_prefix='!', intents=bot_intents)

#client = discord.Client(intents=intents)

def get_crypto_price(coin_name: str):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin_name}USDT"
    print(url)
    response = requests.get(url).json()
    return float(response["price"])

'''
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("Got message: ", message.content.lower())

    if "!gp" in message.content.lower():
        msg = message.content.lower()
        coin_name = msg.split("!gp ")[-1]
        coin_name = coin_name.removesuffix(" <@" + str(client.user.id) + ">").strip().upper()
        print(coin_name)

         btc_price = get_crypto_price(coin_name=coin_name)
       await message.channel.send(f"current price of {coin_name} is {btc_price}$")
'''

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="hi")
async def say_hi(ctx):
    await ctx.send(f"Moin Meister!")
    

@bot.command(name="gp")
async def get_price(ctx, coin_name: str = None):
    if not coin_name:
        await ctx.send("Please provide a cryptocurrency name. Usage: `!gp <coin_name>`")
        return
    
    btc_price = get_crypto_price(coin_name=coin_name)
    if btc_price:
        await ctx.send(f"The current price of {coin_name} is ${btc_price}.")
    else:
        await ctx.send(f"Could not retrieve the price for {coin_name}.")

#client.run(TOKEN)
bot.run(TOKEN)