from research.market_data import MarketQuote
from research.symbols import ResearchSymbol


DISCLAIMER = "This is research information, not financial advice."


def format_research_report(
    symbol: ResearchSymbol,
    price: float | None = None,
    quote: MarketQuote | None = None,
) -> str:
    lines = [
        f"Research update: {symbol.display_symbol}",
        f"Asset type: {symbol.asset_type}",
    ]

    if quote is not None:
        lines.append(f"Price: ${quote.price:,.2f}")
        if quote.change is not None and quote.change_percent is not None:
            lines.append(
                f"Daily change: {_format_signed_currency(quote.change)} ({quote.change_percent:+.2f}%)"
            )
        lines.append(
            "Summary: Basic stock quote data is available. Full research pipeline is not enabled yet."
        )
    elif symbol.asset_type == "crypto" and price is not None:
        lines.extend(
            [
                f"Price: ${price:,.2f}",
                "Summary: Basic crypto price data is available. Full research pipeline is not enabled yet.",
            ]
        )
    elif symbol.asset_type == "stock":
        lines.append("Stock data provider is not configured yet.")
    else:
        lines.append("Price data is not available yet.")

    lines.append(DISCLAIMER)
    return "\n".join(lines)


def _format_signed_currency(value: float) -> str:
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.2f}"
