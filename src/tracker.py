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

# Track all tasks in an array
tasks = {}

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
    global tasks
    if not coin_name:
        await ctx.send("Please provide a cryptocurrency name. Usage: `!gpp <coin_name>`")
        return
    
    if coin_name in tasks:
        ctx.send(f"There is already a task running for {coin_name}")
        return
    
    tasks[coin_name] = bot.loop.create_task(get_crypto_price_periodically(ctx, coin_name))


async def get_crypto_price_periodically(ctx, coin_name: str):
    try:
        while True:
            current_price = get_crypto_price(coin_name=coin_name)
            await ctx.send(f"The current price of {coin_name} is ${current_price}.")
            await asyncio.sleep(10)
    except asyncio.CancelledError:
        await ctx.send(f"Task for {coin_name} has been stopped due to problems.")
        raise
    finally:
        tasks.pop(coin_name, None)


@bot.command(name="stop")
async def stop_task(ctx, coin_name: str = None):
    global tasks
    if coin_name not in tasks:
        await ctx.send("The periodic task is not running you idiot!")
    else:
        tasks[coin_name].cancel()
        await ctx.send("Stopping the periodic task for {coin_name}.")


@bot.command(name="list")
async def list_tasks(ctx):
    """
    Lists all currently running tasks.
    Usage: !list
    """
    if not tasks:
        await ctx.send("No tasks are currently running.")
    else:
        task_list = "\n".join(tasks.keys())
        await ctx.send(f"Currently running tasks:\n{task_list}")
            


#client.run(TOKEN)
bot.run(TOKEN)