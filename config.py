# config.py
import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_path = Path.home() / ".productivity_dashboard" / "config.json"
        self.config_dir = self.config_path.parent
        self.config = self.load_config()
    
    def load_config(self):
        if not self.config_path.exists():
            return self.create_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.create_default_config()
    
    def create_default_config(self):
        default_config = {
            "weather": {
                "api_key": "",
                "city": "London",
                "units": "metric"
            },
            "crypto": {
                "coins": ["bitcoin", "ethereum"]
            },
            "focus_mode": {
                "blocked_sites": ["facebook.com", "twitter.com", "youtube.com", "reddit.com"]
            }
        }
        
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        return default_config
    
    def setup(self):
        from rich.console import Console
        from rich.prompt import Prompt
        
        console = Console()
        console.print("Setting up Productivity Dashboard...", style="bold green")
        
        # Weather API setup
        console.print("\nWeather Configuration", style="bold underline")
        self.config["weather"]["api_key"] = Prompt.ask(
            "Enter your OpenWeatherMap API key", 
            default=self.config["weather"]["api_key"]
        )
        self.config["weather"]["city"] = Prompt.ask(
            "Enter your city", 
            default=self.config["weather"]["city"]
        )
        
        # Crypto setup
        console.print("\nCryptocurrency Configuration", style="bold underline")
        coins = Prompt.ask(
            "Enter cryptocurrencies to track (comma-separated)", 
            default=",".join(self.config["crypto"]["coins"])
        )
        self.config["crypto"]["coins"] = [coin.strip() for coin in coins.split(",")]
        
        # Save configuration
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        
        console.print("Configuration saved successfully!", style="green")
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default