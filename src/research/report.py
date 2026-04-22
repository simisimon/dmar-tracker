from research.symbols import ResearchSymbol


DISCLAIMER = "This is research information, not financial advice."


def format_research_report(symbol: ResearchSymbol, price: float | None = None) -> str:
    lines = [
        f"Research update: {symbol.display_symbol}",
        f"Asset type: {symbol.asset_type}",
    ]

    if symbol.asset_type == "crypto" and price is not None:
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
