import apprise
from typing import Dict, Any
from app.plugins.base import BaseNotificationChannel

class AppriseChannel(BaseNotificationChannel):
    
    @classmethod
    def get_plugin_id(cls) -> str:
        return "apprise"
        
    @classmethod
    def get_name(cls) -> str:
        return "Apprise Meta-Channel"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "urls": {
                    "type": "string",
                    "title": "Apprise URLs",
                    "description": "Comma-separated Apprise URLs (e.g. tgram://bot_token/chat_id, slack://...)",
                    "format": "textarea"
                }
            },
            "required": ["urls"]
        }
        
    @classmethod
    def get_notification_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "title": {"type": "string", "title": "Title"},
                "message": {"type": "string", "title": "Message", "format": "textarea"},
                "type": {
                    "type": "string", 
                    "title": "Notification Type", 
                    "enum": ["info", "success", "warning", "failure"],
                    "default": "info"
                }
            },
            "required": ["message"]
        }
        
    def validate_config(self) -> bool:
        return bool(self.config.get("urls"))
        
    async def send(self, title: str, payload: str, parameters: Dict[str, Any], **kwargs) -> bool:
        urls = self.config.get("urls", "").split(",")
        if not urls:
            return False
            
        apobj = apprise.Apprise()
        for url in urls:
            url = url.strip()
            if url:
                apobj.add(url)
                
        # Get notification parameters
        msg_title = parameters.get("title", title)
        msg_body = parameters.get("message", payload) or "KeepMeUpdated Apprise Notification"
        msg_type_str = parameters.get("type", "info")
        
        # Map string type to apprise notify type
        notify_type = apprise.NotifyType.INFO
        if msg_type_str == "success":
            notify_type = apprise.NotifyType.SUCCESS
        elif msg_type_str == "warning":
            notify_type = apprise.NotifyType.WARNING
        elif msg_type_str == "failure":
            notify_type = apprise.NotifyType.FAILURE
            
        return await apobj.async_notify(
            body=msg_body,
            title=msg_title,
            notify_type=notify_type
        )
