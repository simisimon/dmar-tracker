import aiohttp
import asyncio

async def fetch_data(session, url):
    """Fetch data from the given URL."""
    async with session.get(url) as response:
        # Process the response
        data = await response.json()
        print(data)  # Or handle the data as needed

async def periodic_task(url, interval):
    """Run the fetch_data function periodically."""
    async with aiohttp.ClientSession() as session:
        while True:
            await fetch_data(session, url)
            await asyncio.sleep(interval)