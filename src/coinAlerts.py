# New Class that will be used to track the alerts for each coin set for a specific user
# Idea: create a dictionary that maps the user_id to a list of CoinAlerts objects
class CoinAlerts:
    def __init__(self, coin_name: str, above: float = 0.0, below: float = 0.0):
        self.coin_name = coin_name
        self.above = above
        self.below = below