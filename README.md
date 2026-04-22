# dmar-tracker

Discord bot for tracking stock and cryptocurrency prices.

## Discord Commands

The bot uses `!` as its command prefix.

| Command | Description |
| --- | --- |
| `!hi` | Sends a simple greeting for testing whether the bot is responding. |
| `!gp <coin>` | Gets the current Binance USDT price for a coin, such as `!gp BTC`. |
| `!research <symbol>` | Prints a first research report for a stock or crypto symbol, such as `!research BTC` or `!research AAPL`. Crypto uses Binance price data; stocks use `yfinance`. |
| `!gpp <coin>` | Starts a periodic price check for a coin every 10 seconds. |
| `!stop <coin>` | Stops the periodic price check for the selected coin. |
| `!list` | Lists coins that currently have periodic price checks running. |
| `!setalert <coin> <above> <below>` | Sets an alert for a coin when the price reaches the upper or lower threshold. |
| `!removealert <coin>` | Removes your alert for the selected coin. |
| `!listalerts` | Lists the alerts you have configured. |
| `!whoami` | Replies with a mention of your Discord user account for debugging. |
| `!load <cog>` | Loads a cog from `src/cogs/`, for example `!load periodic_tasks`. |
| `!unload <cog>` | Unloads a loaded cog, for example `!unload periodic_tasks`. |

Coin symbols are converted to uppercase and queried as `<COIN>USDT` on Binance.
