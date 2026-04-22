import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from research.symbols import normalize_symbol


class NormalizeSymbolTests(unittest.TestCase):
    def test_normalize_crypto_symbol_adds_usdt_pair(self):
        symbol = normalize_symbol("btc")

        self.assertEqual(symbol.input_symbol, "btc")
        self.assertEqual(symbol.display_symbol, "BTC")
        self.assertEqual(symbol.asset_type, "crypto")
        self.assertEqual(symbol.provider_symbol, "BTCUSDT")

    def test_normalize_existing_crypto_pair_keeps_pair(self):
        symbol = normalize_symbol("ethusdt")

        self.assertEqual(symbol.display_symbol, "ETH")
        self.assertEqual(symbol.asset_type, "crypto")
        self.assertEqual(symbol.provider_symbol, "ETHUSDT")

    def test_normalize_stock_symbol_keeps_ticker(self):
        symbol = normalize_symbol("aapl")

        self.assertEqual(symbol.display_symbol, "AAPL")
        self.assertEqual(symbol.asset_type, "stock")
        self.assertEqual(symbol.provider_symbol, "AAPL")

    def test_normalize_symbol_rejects_empty_input(self):
        with self.assertRaisesRegex(ValueError, "Symbol is required."):
            normalize_symbol("   ")


if __name__ == "__main__":
    unittest.main()
