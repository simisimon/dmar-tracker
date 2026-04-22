# Stock Market Research Agent Transformation Plan

## Goal

Transform the current Discord price-tracking bot into a stock and crypto research agent that periodically collects market data, analyzes it, and prints concise research summaries for configured symbols.

The first version should focus on reliable data collection, repeatable analysis, and clear Discord output. Advanced AI summarization can be added after the data pipeline is stable.

## Current Starting Point

The repository currently contains a small Python Discord bot in `src/`:

- `src/tracker.py`: Discord bot startup, token loading, and cog loading.
- `src/cogs/periodic_tasks.py`: Existing Discord commands, periodic crypto price checks, and alert handling.
- `src/coinAlerts.py`: Simple alert data object.
- `src/main.py`: Standalone Binance BTC price check.
- `src/helperFunctions.py`: Experimental async HTTP helper code.

The current bot fetches Binance spot prices and responds to Discord commands. It does not yet have a clean separation between Discord commands, data collection, analysis, storage, and reporting.

## Target Capabilities

1. Track configured stock tickers and crypto symbols.
2. Periodically collect price, volume, and basic market data.
3. Collect relevant web/news data for each tracked symbol.
4. Analyze price movement, trend, volatility, alerts, and noteworthy news.
5. Print a readable research summary in Discord.
6. Support manual commands such as `!research AAPL` or `!research BTC`.
7. Store configured symbols and recent snapshots so the bot can compare current data to previous data.

## Proposed Module Structure

Create a clearer application layout under `src/`:

```text
src/
  tracker.py
  config.py
  bot/
    __init__.py
    research_cog.py
    alert_cog.py
  research/
    __init__.py
    symbols.py
    scheduler.py
    pipeline.py
    report.py
  data_providers/
    __init__.py
    crypto_prices.py
    stock_prices.py
    news.py
    web_search.py
    x_posts.py
  analysis/
    __init__.py
    market_metrics.py
    sentiment.py
    social_signals.py
    research_summary.py
  storage/
    __init__.py
    repository.py
    sqlite_repository.py
  tests/
```

## Step-by-Step Transformation

### Step 1: Stabilize Configuration

Create `src/config.py` to load environment variables in one place.

Required settings:

- `DISCORD_TOKEN`
- `DISCORD_GUILD` if guild-specific behavior is needed
- `RESEARCH_INTERVAL_SECONDS`, defaulting to a safe value such as `3600`
- Optional API keys for stock, news, or AI providers

Move `load_dotenv()` and direct `os.getenv()` calls out of `tracker.py`.

### Step 2: Split Discord Bot Code from Research Logic

Keep `src/tracker.py` responsible only for starting the Discord bot and loading cogs.

Move command handlers into:

- `src/bot/research_cog.py`
- `src/bot/alert_cog.py`

The cogs should call services from `src/research/` instead of fetching data directly.

### Step 3: Introduce Symbol Management

Create `src/research/symbols.py`.

Responsibilities:

- Normalize symbols such as `btc`, `BTC`, `BTCUSDT`, and `AAPL`.
- Distinguish crypto symbols from stock tickers.
- Store metadata such as display name, asset type, and quote currency.

Example normalized symbols:

```text
BTC -> crypto, BTCUSDT
AAPL -> stock, AAPL
ETH -> crypto, ETHUSDT
```

### Step 4: Add Data Provider Interfaces

Create provider modules with small, predictable functions.

Needed modules:

- `data_providers/crypto_prices.py`: Fetch Binance crypto price and volume data.
- `data_providers/stock_prices.py`: Fetch stock quote and historical price data from a chosen stock data API.
- `data_providers/news.py`: Fetch financial news from RSS feeds or a news API.
- `data_providers/web_search.py`: Optional provider for broader web research.

Each provider should return plain Python dictionaries or dataclasses instead of Discord messages.

### Step 5: Add Storage

Create `storage/repository.py` as an interface and `storage/sqlite_repository.py` as the first implementation.

Store:

- Tracked symbols.
- Latest market snapshots.
- Recent research reports.
- Alert thresholds.

Use SQLite first because it is local, simple, and enough for a single Discord bot.

### Step 6: Build Market Analysis Modules

Create `analysis/market_metrics.py`.

Calculate:

- Current price.
- 24-hour change.
- Recent high and low.
- Simple moving averages.
- Volatility estimate.
- Volume change when available.

Create `analysis/sentiment.py`.

Start with simple rule-based sentiment from news headlines:

- Positive keywords: `beats`, `upgrade`, `growth`, `profit`, `approval`.
- Negative keywords: `misses`, `downgrade`, `lawsuit`, `loss`, `investigation`.

Do not depend on AI for the first version.

### Step 7: Build the Research Pipeline

Create `research/pipeline.py`.

Pipeline flow:

1. Receive a symbol.
2. Normalize the symbol.
3. Fetch market data.
4. Fetch news and web data.
5. Save the raw snapshot.
6. Run analysis.
7. Generate a research summary.
8. Save and return the report.

This pipeline should be usable by both manual Discord commands and scheduled tasks.

### Step 8: Create Report Formatting

Create `research/report.py`.

The report should be concise and Discord-friendly.

Example output:

```text
Research update: BTC
Price: $64,250.12
24h change: +2.4%
Trend: Above short moving average
Volatility: Medium
News tone: Mixed
Key headlines:
- ...
- ...
Summary: BTC is showing positive short-term momentum, but recent news is mixed.
```

Add a clear note that output is research information, not financial advice.

### Step 9: Add New Discord Commands

Add commands in `bot/research_cog.py`:

- `!research <symbol>`: Run an immediate research report.
- `!track <symbol>`: Add a symbol to periodic research.
- `!untrack <symbol>`: Remove a tracked symbol.
- `!tracked`: List tracked symbols.
- `!researchnow`: Run reports for all tracked symbols.
- `!setinterval <seconds>`: Change the research interval if allowed.

Keep existing commands working during the transition where practical.

### Step 10: Add Scheduling

Create `research/scheduler.py`.

Responsibilities:

- Start one background task for periodic research.
- Load tracked symbols from storage.
- Run the research pipeline for each symbol.
- Send reports to a configured Discord channel.
- Avoid duplicate tasks for the same symbol.
- Handle provider failures without stopping the scheduler.

### Step 11: Add Error Handling and Rate Limits

Add predictable handling for:

- Invalid symbols.
- API timeouts.
- HTTP errors.
- Missing API keys.
- Provider rate limits.
- Empty news results.

Use short user-facing Discord messages and more detailed console logs.

### Step 12: Add Tests

Create a `tests/` directory.

Suggested test files:

- `tests/test_symbols.py`
- `tests/test_market_metrics.py`
- `tests/test_sentiment.py`
- `tests/test_report.py`
- `tests/test_pipeline.py`

Mock all network calls. Tests should verify that a report can be produced from fixed sample data without Discord or live API access.

### Step 13: Update Documentation

Update `README.md` with:

- Setup instructions.
- Required `.env` variables.
- Research commands.
- Example output.
- Data provider notes.
- Disclaimer that generated summaries are not financial advice.

Update `AGENTS.md` after the module structure changes so contributors follow the new layout.

### Step 14: Add Optional X.com Account Signal Collection

Add X.com collection as an optional provider after the core research pipeline works.

Preferred module:

- `data_providers/x_posts.py`: Fetch recent posts for configured X.com accounts.

Preferred analysis module:

- `analysis/social_signals.py`: Analyze account activity, post tone, ticker mentions, engagement changes, and repeated themes.

The recommended implementation path is API-first. Use the official X API when available, because direct HTML scraping is brittle, may break when X changes its frontend, and may conflict with platform access rules. If scraping is still used, keep it isolated behind the same provider interface, make it configurable, respect rate limits, avoid login/session workarounds, and store only the minimum post metadata needed for research.

Store optional X.com data separately:

- Tracked X.com account handles.
- Recent post snapshots.
- Extracted ticker or crypto mentions.
- Per-account signal summaries.

Example signal output:

```text
X account signals:
- @example posted 4 times in the last 24h
- Tone: Positive
- Mentions: BTC, ETF, liquidity
- Engagement: Above recent baseline
```

## Implementation Phases

### Phase 1: Refactor Without New Features

- Add `config.py`.
- Move Discord commands into cogs.
- Preserve existing price and alert behavior.
- Add basic tests around symbol normalization and report formatting.

### Phase 2: Manual Research Reports

- Add data provider interfaces.
- Add crypto and stock price providers.
- Add market metric analysis.
- Add `!research <symbol>`.

### Phase 3: News and Web Collection

- Add news provider.
- Add simple sentiment analysis.
- Add headlines to research reports.
- Add tests with mocked news data.

### Phase 4: Persistent Tracking

- Add SQLite storage.
- Add `!track`, `!untrack`, and `!tracked`.
- Persist tracked symbols across restarts.

### Phase 5: Periodic Agent Behavior

- Add scheduler.
- Run research automatically for tracked symbols.
- Send reports to a configured Discord channel.
- Add failure handling and rate-limit protection.

### Phase 6: Optional AI Analysis Layer

- Add an `analysis/research_summary.py` interface.
- Keep rule-based summaries as the fallback.
- Add an optional AI provider only after deterministic reports work.
- Store prompts and provider configuration outside Discord command handlers.

### Phase 7: Optional X.com Signals

- Add `data_providers/x_posts.py`.
- Add account configuration for tracked X.com handles.
- Add `analysis/social_signals.py`.
- Include X.com account signals in research reports when enabled.
- Keep this feature disabled by default unless API access or scraping permissions are configured.

## Recommended Dependencies

Start with:

```text
discord.py
python-dotenv
requests
aiohttp
pytest
```

Likely additions:

```text
pydantic
feedparser
beautifulsoup4
```

Optional X.com scraping additions, only if direct scraping is chosen:

```text
playwright
```

Choose one stock market data provider before implementation. Good provider candidates include Alpha Vantage, Polygon, Finnhub, Twelve Data, or Yahoo Finance-style libraries. The choice affects API keys, rate limits, and licensing.

## Verification Checklist

- Bot starts with `python src/tracker.py`.
- `!research BTC` returns a crypto research report.
- `!research AAPL` returns a stock research report.
- `!track BTC` persists across restarts.
- Scheduler produces reports at the configured interval.
- Provider failures produce readable Discord errors.
- Tests pass without network access.
- Secrets stay in `.env` and are not logged.

## Open Decisions Before Implementation

1. Which stock data provider should be used?
2. Which news source should be used first: RSS feeds, a news API, or general web scraping?
3. Should reports be sent to the command channel, a configured research channel, or direct messages?
4. Should the bot analyze only tracked symbols, or also market-wide watchlists?
5. Should AI-generated summaries be included in version one or added later?
6. Should X.com signals use the official API, direct scraping, or be excluded until access rules are confirmed?
7. Which X.com accounts should be tracked for each stock or crypto symbol?
