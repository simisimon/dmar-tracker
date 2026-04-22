import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from research.market_data import MarketQuote


class MarketQuoteTests(unittest.TestCase):
    def test_calculates_change_percent_from_previous_close(self):
        quote = MarketQuote(
            symbol="AAPL",
            asset_type="stock",
            price=210.0,
            currency="USD",
            previous_close=200.0,
        )

        self.assertEqual(quote.change, 10.0)
        self.assertEqual(quote.change_percent, 5.0)

    def test_missing_previous_close_returns_no_change_percent(self):
        quote = MarketQuote(
            symbol="BTC",
            asset_type="crypto",
            price=64250.12,
            currency="USD",
            previous_close=None,
        )

        self.assertIsNone(quote.change)
        self.assertIsNone(quote.change_percent)


if __name__ == "__main__":
    unittest.main()
