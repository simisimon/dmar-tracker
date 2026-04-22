# Repository Guidelines

## Project Structure & Module Organization

This repository contains a small Python Discord bot for tracking cryptocurrency prices. Source code lives in `src/`. The bot entry point is `src/tracker.py`, Discord cogs live in `src/cogs/`, and alert data helpers currently live in `src/coinAlerts.py`. `src/main.py` is a simple Binance price-check script. There is no dedicated `tests/` directory yet. Avoid committing generated files such as `__pycache__/` or local environment files.

## Build, Test, and Development Commands

Create and activate a local virtual environment before installing dependencies:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install discord.py python-dotenv requests aiohttp
```

Run the Discord bot from `src/` so cog discovery can find `./cogs`:

```powershell
cd src
python tracker.py
```

Run the standalone Binance price check with:

```powershell
python src/main.py
```

For a quick syntax check, run:

```powershell
python -m py_compile src\tracker.py src\main.py src\coinAlerts.py src\cogs\periodic_tasks.py
```

## Coding Style & Naming Conventions

Use Python 3 style with 4-space indentation. Keep Discord command handlers asynchronous and name command functions with lowercase `snake_case`. Existing files use module names such as `tracker.py` and `periodic_tasks.py`; prefer lowercase module names for new files. Keep bot command names short and user-facing, for example `gp`, `setalert`, and `listalerts`. Add comments only when they clarify non-obvious Discord, task, or alert behavior.

## Testing Guidelines

No test framework is configured yet. For new logic, prefer adding `pytest` tests under a new `tests/` directory and isolate network calls to Binance behind mockable helper functions. Name tests after behavior, for example `test_get_crypto_price_parses_binance_response`. At minimum, run the `py_compile` command above before submitting changes.

## Commit & Pull Request Guidelines

Recent commit messages are short, lowercase summaries such as `switched endpoint` and `fixed problem with above or below being None`. Keep commits focused and describe the behavior changed. Pull requests should include a short description, commands run, any required `.env` changes, and screenshots or Discord command transcripts when user-visible bot behavior changes.

## Security & Configuration Tips

Secrets belong in `.env`, which is ignored by Git. The bot expects `DISCORD_TOKEN` and may use `DISCORD_GUILD`. Do not print tokens or commit local `.env` files. Treat Discord user IDs and alert data as user-specific runtime data.
