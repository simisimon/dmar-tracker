import os
import discord
from discord.ext import commands
import requests

from dotenv import load_dotenv
from discord.ext import commands
from cogs.periodic_tasks import PeriodicTasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#intents = discord.Intents.default()
#intents.typing = False
#intents.presences = False

bot_intents = discord.Intents.all()
#bot_intents.messages = True

bot = commands.Bot(command_prefix='!', intents=bot_intents)

# Track all tasks in a dictionary
tasks = {}

#client = discord.Client(intents=intents)

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

# Load the PeriodicTasks cog
#bot.add_cog(PeriodicTasks(bot))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.load_extension('cogs.periodic_tasks')
    print("Manually loaded periodic_tasks cog")

# Load cogs dynamically
@bot.command(name="load")
#@commands.is_owner()
async def load_cog(ctx, extension):
    try:
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded cog: {extension}")
    except Exception as e:
        await ctx.send(f"Failed to load cog {extension}: {e}")


@bot.command(name="unload")
#@commands.is_owner()
async def unload_cog(ctx, extension):
    try:
        await bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Unloaded cog: {extension}")
    except Exception as e:
        await ctx.send(f"Failed to unload cog {extension}: {e}")

            
# Automatically load cogs on startup
if __name__ == "__main__":
    import os
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
            except Exception as e:
                    print(f"Failed to load cog {filename}: {e}")


#client.run(TOKEN)
bot.run(TOKEN)