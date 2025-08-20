# crypto.py
import requests
from rich.console import Console

class CryptoAPI:
    def __init__(self, config):
        self.config = config
        self.base_url = "https://api.coingecko.com/api/v3"
        self.coins = self.config.get("crypto.coins", ["bitcoin", "ethereum"])
        self.console = Console()
    
    def get_crypto_prices(self):
        try:
            coin_ids = ",".join(self.coins)
            params = {
                "ids": coin_ids,
                "vs_currencies": "usd",
                "include_24hr_change": "true"
            }
            
            response = requests.get(
                f"{self.base_url}/simple/price",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            result = {}
            
            for coin in self.coins:
                if coin in data:
                    result[coin.title()] = {
                        "price": data[coin]["usd"],
                        "change_24h": data[coin]["usd_24h_change"]
                    }
            
            return result
            
        except requests.exceptions.RequestException as e:
            self.console.print(f"Crypto API error: {e}", style="red")
            return None
        except KeyError as e:
            self.console.print(f"Crypto data parsing error: {e}", style="red")
            return None