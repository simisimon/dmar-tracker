import requests

def get_get_btc_price():
    url = f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url).json()
    print(float(response["price"]))

if __name__ == "__main__":
    get_get_btc_price()