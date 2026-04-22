from research.market_data import MarketQuote


def build_stock_quote(symbol: str, fast_info) -> MarketQuote:
    price = _read_fast_info_value(fast_info, "last_price")
    if price is None:
        raise ValueError(f"No stock price returned for {symbol.upper()}.")

    return MarketQuote(
        symbol=symbol.upper(),
        asset_type="stock",
        price=float(price),
        currency=_read_fast_info_value(fast_info, "currency") or "USD",
        previous_close=_optional_float(
            _read_fast_info_value(fast_info, "previous_close")
        ),
    )


def get_stock_quote(symbol: str) -> MarketQuote:
    try:
        import yfinance as yf
    except ImportError as error:
        raise RuntimeError(
            "Stock data provider is not installed. Run `pip install -r requirements.txt`."
        ) from error

    ticker = yf.Ticker(symbol.upper())
    return build_stock_quote(symbol, ticker.fast_info)


def _read_fast_info_value(fast_info, key: str):
    if isinstance(fast_info, dict):
        return fast_info.get(key)

    try:
        return fast_info[key]
    except (KeyError, TypeError):
        return getattr(fast_info, key, None)


def _optional_float(value) -> float | None:
    if value is None:
        return None
    return float(value)
