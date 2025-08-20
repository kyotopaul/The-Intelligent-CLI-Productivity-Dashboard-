# weather.py
import requests
from rich.console import Console

class WeatherAPI:
    def __init__(self, config):
        self.config = config
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.api_key = self.config.get("weather.api_key")
        self.city = self.config.get("weather.city")
        self.units = self.config.get("weather.units", "metric")
        self.console = Console()
    
    def get_weather(self):
        if not self.api_key:
            self.console.print("Weather API key not configured. Run 'python dashboard.py --setup'", style="red")
            return None
        
        try:
            params = {
                "q": self.city,
                "appid": self.api_key,
                "units": self.units
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "city": self.city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"] * 3.6,  # Convert m/s to km/h
            }
            
        except requests.exceptions.RequestException as e:
            self.console.print(f"Weather API error: {e}", style="red")
            return None
        except (KeyError, IndexError) as e:
            self.console.print(f"Weather data parsing error: {e}", style="red")
            return None