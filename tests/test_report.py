import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from research.report import format_research_report
from research.market_data import MarketQuote
from research.symbols import normalize_symbol


class FormatResearchReportTests(unittest.TestCase):
    def test_format_crypto_report_with_price(self):
        symbol = normalize_symbol("btc")

        report = format_research_report(symbol, price=64250.12)

        self.assertIn("Research update: BTC", report)
        self.assertIn("Asset type: crypto", report)
        self.assertIn("Price: $64,250.12", report)
        self.assertIn("Full research pipeline is not enabled yet.", report)
        self.assertIn("not financial advice", report)

    def test_format_stock_report_without_provider(self):
        symbol = normalize_symbol("aapl")

        report = format_research_report(symbol, price=None)

        self.assertIn("Research update: AAPL", report)
        self.assertIn("Asset type: stock", report)
        self.assertIn("Stock data provider is not configured yet.", report)
        self.assertIn("not financial advice", report)

    def test_format_stock_report_with_quote(self):
        symbol = normalize_symbol("aapl")
        quote = MarketQuote(
            symbol="AAPL",
            asset_type="stock",
            price=210.0,
            currency="USD",
            previous_close=200.0,
        )

        report = format_research_report(symbol, quote=quote)

        self.assertIn("Research update: AAPL", report)
        self.assertIn("Asset type: stock", report)
        self.assertIn("Price: $210.00", report)
        self.assertIn("Daily change: +$10.00 (+5.00%)", report)
        self.assertIn("Basic stock quote data is available.", report)


if __name__ == "__main__":
    unittest.main()
