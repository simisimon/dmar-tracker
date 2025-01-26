import discord
from discord.ext import commands
import asyncio
import requests


class PeriodicTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks = {}  # Dictionary to track running tasks by name

    @commands.command(name="hi")
    async def say_hi(self, ctx):
        await ctx.send(f"Moin Meister!")        

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



    @commands.command(name="gpp")
    async def get_price_periodically(self, ctx, coin_name: str = None):
        if not coin_name:
            await ctx.send("Please provide a cryptocurrency name. Usage: `!gpp <coin_name>`")
            return
        
        if coin_name in self.tasks:
            ctx.send(f"There is already a task running for {coin_name}")
            return
        
        self.tasks[coin_name] = self.bot.loop.create_task(self.get_crypto_price_periodically(ctx, coin_name))


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


    @commands.command(name="stop")
    async def stop_task(self, ctx, coin_name: str = None):
        if coin_name not in self.tasks:
            await ctx.send("The periodic task is not running you idiot!")
        else:
            self.tasks[coin_name].cancel()
            await ctx.send("Stopping the periodic task for {coin_name}.")


    @commands.command(name="list")
    async def list_tasks(self, ctx):
        """
        Lists all currently running tasks.
        Usage: !list
        """
        if not self.tasks:
            await ctx.send("No tasks are currently running.")
        else:
            task_list = "\n".join(self.tasks.keys())
            await ctx.send(f"Currently running tasks:\n{task_list}")

    def get_crypto_price(self, coin_name: str):
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin_name}USDT"
        print(url)
        response = requests.get(url).json()
        return float(response["price"])


# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(PeriodicTasks(bot))