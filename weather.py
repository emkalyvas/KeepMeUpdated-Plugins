import httpx
from typing import Dict, Any
from app.plugins.base import BaseDataSourcePlugin

class OpenWeatherMapPlugin(BaseDataSourcePlugin):
    @classmethod
    def get_plugin_id(cls) -> str:
        return "weather_owm"
        
    @classmethod
    def get_name(cls) -> str:
        return "OpenWeatherMap"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "api_key": {
                    "type": "string",
                    "title": "API Key",
                    "description": "Your OpenWeatherMap API Key"
                },
                "location": {
                    "type": "string",
                    "title": "Location",
                    "description": "City name (e.g. 'London,UK')"
                },
                "units": {
                    "type": "string",
                    "title": "Units",
                    "enum": ["metric", "imperial", "standard"],
                    "default": "metric"
                }
            },
            "required": ["api_key", "location"]
        }
        
    @classmethod
    def get_context_schema(cls) -> list:
        return [
            {"name": "temperature", "description": "Current temperature", "example": "22°C"},
            {"name": "feels_like", "description": "Feels like temperature", "example": "24°C"},
            {"name": "weatherCondition", "description": "Main weather condition", "example": "Clear"},
            {"name": "weatherDescription", "description": "Detailed weather description", "example": "clear sky"},
            {"name": "humidity", "description": "Humidity percentage", "example": "50%"}
        ]
        
    def validate_config(self) -> bool:
        return bool(self.config.get("api_key") and self.config.get("location"))
        
    async def fetch_context(self) -> Dict[str, Any]:
        api_key = self.config.get("api_key")
        location = self.config.get("location")
        units = self.config.get("units", "metric")
        
        unit_symbol = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units}"
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                data = resp.json()
                
                return {
                    "temperature": f"{data['main']['temp']}{unit_symbol}",
                    "feels_like": f"{data['main']['feels_like']}{unit_symbol}",
                    "weatherCondition": data['weather'][0]['main'],
                    "weatherDescription": data['weather'][0]['description'],
                    "humidity": f"{data['main']['humidity']}%"
                }
            except Exception as e:
                print(f"Failed to fetch weather data: {e}")
                return {
                    "temperature": "N/A",
                    "feels_like": "N/A",
                    "weatherCondition": "N/A",
                    "weatherDescription": "N/A",
                    "humidity": "N/A"
                }
