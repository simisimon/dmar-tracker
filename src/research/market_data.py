from dataclasses import dataclass


@dataclass(frozen=True)
class MarketQuote:
    symbol: str
    asset_type: str
    price: float
    currency: str = "USD"
    previous_close: float | None = None

    @property
    def change(self) -> float | None:
        if self.previous_close is None:
            return None
        return self.price - self.previous_close

    @property
    def change_percent(self) -> float | None:
        if self.previous_close in (None, 0):
            return None
        return (self.change / self.previous_close) * 100
