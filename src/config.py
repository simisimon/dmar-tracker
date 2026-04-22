import os

from dotenv import load_dotenv


load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = os.getenv("DISCORD_GUILD")
RESEARCH_INTERVAL_SECONDS = int(os.getenv("RESEARCH_INTERVAL_SECONDS", "3600"))
