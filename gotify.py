
import urllib.request
import json
from typing import Dict, Any
from .base import BaseNotificationChannel

class GotifyChannel(BaseNotificationChannel):
    
    @classmethod
    def get_plugin_id(cls) -> str:
        return "gotify"
        
    @classmethod
    def get_name(cls) -> str:
        return "Gotify"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "server_url": {"type": "string", "title": "Gotify Server URL"},
                "app_token": {"type": "string", "title": "Application Token", "format": "password"}
            },
            "required": ["server_url", "app_token"]
        }
        
    @classmethod
    def get_notification_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string", "title": "Title"},
                "message": {"type": "string", "title": "Message", "format": "textarea"},
                "priority": {"type": "integer", "title": "Priority (0-10)", "default": 5}
            },
            "required": ["message"]
        }
        
    def validate_config(self) -> bool:
        return bool(self.config.get("server_url") and self.config.get("app_token"))
        
    async def send(self, title: str, payload: str, parameters: Dict[str, Any], **kwargs) -> bool:
        server_url = self.config.get("server_url", "").strip().rstrip("/")
        app_token = self.config.get("app_token", "").strip()
        
        if not server_url or not app_token:
            return False
            
        url = f"{server_url}/message"
        data = {
            "title": parameters.get("title", title),
            "message": parameters.get("message", payload or ""),
            "priority": parameters.get("priority", 5)
        }
        
        try:
            headers = {
                "Content-Type": "application/json",
                "X-Gotify-Key": app_token,
                "Authorization": f"Bearer {app_token}"
            }
            req = urllib.request.Request(url, json.dumps(data).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req) as response:
                return response.status == 200
        except Exception as e:
            print(f"Gotify send failed: {e}")
            return False
