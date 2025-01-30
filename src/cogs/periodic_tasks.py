import discord
from discord.ext import commands
import asyncio
import requests
from coinAlerts import CoinAlerts


class PeriodicTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks = {} # Dictionary to track running tasks by coin_name
        self.coinAlertsPerUser = {}  # Dictionary to track set alerts for each user
        #self.tasksPerUser = {}
        #self.users = {}

    # simple "Hi" command, mostly used for debugging
    @commands.command(name="hi")
    async def say_hi(self, ctx):
        await ctx.send(f"Moin Meister!")        

    # gp command, used to get the current price of a cryptocurrency
    # Usage: !gp <name of the coin>
    @commands.command(name="gp")
    async def get_price(self, ctx, coin_name: str = None):
        if not coin_name:
            await ctx.send("Please provide a cryptocurrency name. Usage: `!gp <coin_name>`")
            return
        
        btc_price = self.get_crypto_price(coin_name=coin_name)
        if btc_price:
            await ctx.send(f"The current price of {coin_name} is ${btc_price}.")
        else:
            await ctx.send(f"Could not retrieve the price for {coin_name}.")

    # setalert command, used to set an setalert for a given cryprocurrency
    # you need to provide the coin name, the price above which the setalert should trigger
    # and the price below which the setalert should trigger
    # Usage: !setalert <coin_name> <above> <below>
    @commands.command(name="setalert")
    async def set_alert(self, ctx, coin_name: str, above: float, below: float):
        if not coin_name:
            await ctx.send("Please provide a cryptocurrency name. Usage: `!setalert <coin_name> <above> <below>`")
            return
        
        if coin_name not in self.tasks:
            self.tasks[coin_name] = self.bot.loop.create_task(self.get_crypto_price_periodically(ctx, coin_name))

        if ctx.author.id not in self.coinAlertsPerUser:
            self.coinAlertsPerUser[ctx.author.id] = []

        self.coinAlertsPerUser[ctx.author.id].append(CoinAlerts(coin_name, above, below))


    # gpp command, used to add an automatic task that fetches the price of the given cryptocurrency every 10 seconds
    # Usage: !gpp <name of the coin>
    @commands.command(name="gpp")
    async def get_price_periodically(self, ctx, coin_name: str = None):
        if not coin_name:
            await ctx.send("Please provide a cryptocurrency name. Usage: `!gpp <coin_name>`")
            return
        
        if coin_name in self.tasks:
            ctx.send(f"There is already a task running for {coin_name}")
            return
        
        # commented out line was used to allow more than one task per coin, but it doesnt make sense to have more than 1 task per coin for now
        #self.tasks[f"{ctx.author.id}{coin_name}"] = self.bot.loop.create_task(self.get_crypto_price_periodically(ctx, coin_name))
        self.tasks[coin_name] = self.bot.loop.create_task(self.get_crypto_price_periodically(ctx, coin_name))


    # helper function used for the gpp command
    async def get_crypto_price_periodically(self, ctx, coin_name: str):
        try:
            while True:
                current_price = self.get_crypto_price(coin_name=coin_name)
                await ctx.send(f"The current price of {coin_name} is ${current_price}.")
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            await ctx.send(f"Task for {coin_name} has been stopped due to problems.")
            raise
        finally:
            self.tasks.pop(coin_name, None)

    # stop command, used to stop the automatic task for a given cryptocurrency
    # Usage: !stop <name of the coin>
    @commands.command(name="stop")
    async def stop_task(self, ctx, coin_name: str = None):
        if coin_name not in self.tasks:
            await ctx.send("The periodic task is not running you idiot!")
        else:
            self.tasks[coin_name].cancel()
            await ctx.send(f"Stopping the periodic task for {coin_name}.")

    # list command, used to list all cryptocurrencies for which automatic tasks are running
    # Usage: !list
    @commands.command(name="list")
    async def list_tasks(self, ctx):
        if not self.tasks:
            await ctx.send("No tasks are currently running.")
        else:
            task_list = "\n".join(self.tasks.keys())
            await ctx.send(f"Currently running tasks:\n{task_list}")

    # helper function used to get the price
    def get_crypto_price(self, coin_name: str):
        coin_name = coin_name.upper()
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin_name}USDT"
        print(url)
        response = requests.get(url).json()
        return float(response["price"])


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(PeriodicTasks(bot))