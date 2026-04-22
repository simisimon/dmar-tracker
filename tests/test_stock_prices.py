import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_providers.stock_prices import build_stock_quote


class BuildStockQuoteTests(unittest.TestCase):
    def test_builds_quote_from_yfinance_fast_info(self):
        quote = build_stock_quote(
            "AAPL",
            {
                "last_price": 210.0,
                "currency": "USD",
                "previous_close": 200.0,
            },
        )

        self.assertEqual(quote.symbol, "AAPL")
        self.assertEqual(quote.asset_type, "stock")
        self.assertEqual(quote.price, 210.0)
        self.assertEqual(quote.currency, "USD")
        self.assertEqual(quote.previous_close, 200.0)

    def test_rejects_missing_price(self):
        with self.assertRaisesRegex(ValueError, "No stock price returned for AAPL."):
            build_stock_quote("AAPL", {"currency": "USD"})


if __name__ == "__main__":
    unittest.main()
