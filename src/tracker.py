import os
import discord
import requests
import helperFunctions
import threading
import asyncio

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
task_running = False

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
    threading.Thread(target=say_hi, args=(ctx,)).start()
    await ctx.send(f"Moin Meister!")

@bot.command(name="yo")
async def say_yo(ctx):
    await ctx.send(f"Yo! What's up?")
    

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


@bot.command(name="gpp")
async def get_price_periodically(ctx, coin_name: str = None):
    global task_running
    if not coin_name:
        await ctx.send("Please provide a cryptocurrency name. Usage: `!gpp <coin_name>`")
        return
    
    if not task_running:
        task_running = True
        bot.loop.create_task(get_crypto_price_periodically(ctx, coin_name))
    else:
        await ctx.send("Task is already running dude")


async def get_crypto_price_periodically(ctx, coin_name: str):
    global task_running

    try:
        while task_running:
            current_price = get_crypto_price(coin_name=coin_name)
            await ctx.send(f"The current price of {coin_name} is ${current_price}.")
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        pass
    finally:
        task_running = False


@bot.command(name="stop")
async def stop_task(ctx):
    global task_running
    if task_running:
        task_running = False
        await ctx.send("Stopping the periodic task!")
    else:
        await ctx.send("The periodic task is not running you idiot!")
            


#client.run(TOKEN)
bot.run(TOKEN)