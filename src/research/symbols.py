from dataclasses import dataclass


CRYPTO_SYMBOLS = {
    "BTC",
    "ETH",
    "BNB",
    "SOL",
    "XRP",
    "ADA",
    "DOGE",
    "AVAX",
    "DOT",
    "LINK",
    "LTC",
    "BCH",
    "MATIC",
    "UNI",
}


@dataclass(frozen=True)
class ResearchSymbol:
    input_symbol: str
    display_symbol: str
    asset_type: str
    provider_symbol: str


def normalize_symbol(raw_symbol: str) -> ResearchSymbol:
    input_symbol = raw_symbol
    symbol = raw_symbol.strip().upper()

    if not symbol:
        raise ValueError("Symbol is required.")

    if symbol.endswith("USDT"):
        base_symbol = symbol.removesuffix("USDT")
        return ResearchSymbol(
            input_symbol=input_symbol,
            display_symbol=base_symbol,
            asset_type="crypto",
            provider_symbol=symbol,
        )

    if symbol in CRYPTO_SYMBOLS:
        return ResearchSymbol(
            input_symbol=input_symbol,
            display_symbol=symbol,
            asset_type="crypto",
            provider_symbol=f"{symbol}USDT",
        )

    return ResearchSymbol(
        input_symbol=input_symbol,
        display_symbol=symbol,
        asset_type="stock",
        provider_symbol=symbol,
    )
