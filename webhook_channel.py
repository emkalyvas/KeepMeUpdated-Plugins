import json
import httpx
from typing import Dict, Any
from app.plugins.base import BaseNotificationChannel

class WebhookChannel(BaseNotificationChannel):
    
    @classmethod
    def get_plugin_id(cls) -> str:
        return "webhook"
        
    @classmethod
    def get_name(cls) -> str:
        return "Webhook (HTTP Request)"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "title": "Webhook URL"},
                "method": {"type": "string", "title": "HTTP Method", "enum": ["GET", "POST", "PUT", "PATCH", "DELETE"], "default": "POST"},
                "headers": {"type": "string", "title": "Headers (JSON format)", "format": "textarea", "default": "{\"Content-Type\": \"application/json\"}"}
            },
            "required": ["url"]
        }
        
    @classmethod
    def get_notification_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "payload": {"type": "string", "title": "Body Payload (JSON or text)", "format": "textarea"}
            },
            "required": ["payload"]
        }
        
    def validate_config(self) -> bool:
        return bool(self.config.get("url"))
        
    async def send(self, title: str, payload: str, parameters: Dict[str, Any], **kwargs) -> bool:
        url = self.config.get("url")
        method = self.config.get("method", "POST")
        headers_str = self.config.get("headers", "{}")
        
        msg_payload = parameters.get("payload", payload)
        
        if not url:
            return False
            
        try:
            headers = json.loads(headers_str) if headers_str.strip() else {}
        except json.JSONDecodeError:
            headers = {}
            
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    content=msg_payload.encode('utf-8')
                )
                return 200 <= response.status_code < 300
        except Exception as e:
            print(f"Webhook failed: {e}")
            return False
