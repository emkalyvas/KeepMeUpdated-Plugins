import httpx
from typing import Dict, Any
from app.plugins.base import BaseDataSourcePlugin

class DailyInspirationDataSource(BaseDataSourcePlugin):
    
    @classmethod
    def get_plugin_id(cls) -> str:
        return "inspiration"
        
    @classmethod
    def get_name(cls) -> str:
        return "Daily Inspiration (ZenQuotes)"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "title": "Quote Mode", "enum": ["random", "today"], "default": "random"}
            },
            "required": ["mode"]
        }
        
    @classmethod
    def get_context_schema(cls) -> list:
        return [
            {"name": "quote", "description": "Motivational quote text", "example": "The only way to do great work is to love what you do."},
            {"name": "author", "description": "Author of the quote", "example": "Steve Jobs"}
        ]
        
    def validate_config(self) -> bool:
        return True
        
    async def fetch_context(self) -> Dict[str, Any]:
        mode = self.config.get("mode", "random")
        url = f"https://zenquotes.io/api/{mode}"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data and isinstance(data, list) and len(data) > 0:
                        return {
                            "quote": data[0].get("q", "No quote found"),
                            "author": data[0].get("a", "Unknown")
                        }
        except Exception as e:
            print(f"Inspiration fetch failed: {e}")
            
        return {"quote": "Stay positive and keep coding!", "author": "KeepMeUpdated"}
