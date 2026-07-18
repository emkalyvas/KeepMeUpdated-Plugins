import httpx
from typing import Dict, Any
from app.plugins.base import BaseDataSource

class CoinGeckoDataSource(BaseDataSource):
    
    @classmethod
    def get_plugin_id(cls) -> str:
        return "coingecko"
        
    @classmethod
    def get_name(cls) -> str:
        return "CoinGecko Crypto Tracker"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "coin_id": {"type": "string", "title": "Coin ID (e.g. bitcoin, ethereum)", "default": "bitcoin"},
                "currency": {"type": "string", "title": "Fiat Currency (e.g. usd, eur)", "default": "usd"}
            },
            "required": ["coin_id", "currency"]
        }
        
    def validate_config(self) -> bool:
        return bool(self.config.get("coin_id") and self.config.get("currency"))
        
    async def fetch_data(self) -> Dict[str, Any]:
        coin = self.config.get("coin_id", "bitcoin").lower()
        currency = self.config.get("currency", "usd").lower()
        
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}&include_24hr_change=true"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if coin in data:
                        return {
                            "price": str(data[coin].get(currency, "N/A")),
                            "change_24h": f"{data[coin].get(f'{currency}_24h_change', 0):.2f}%"
                        }
        except Exception as e:
            print(f"CoinGecko fetch failed: {e}")
            
        return {"price": "Error", "change_24h": "Error"}
