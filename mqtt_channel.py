import paho.mqtt.publish as publish
from typing import Dict, Any
from app.plugins.base import BaseNotificationChannel

class MqttChannel(BaseNotificationChannel):
    
    @classmethod
    def get_plugin_id(cls) -> str:
        return "mqtt"
        
    @classmethod
    def get_name(cls) -> str:
        return "MQTT (Home Assistant)"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "broker": {"type": "string", "title": "MQTT Broker Hostname/IP"},
                "port": {"type": "integer", "title": "Port", "default": 1883},
                "username": {"type": "string", "title": "Username (Optional)"},
                "password": {"type": "string", "title": "Password (Optional)", "format": "password"}
            },
            "required": ["broker", "port"]
        }
        
    @classmethod
    def get_notification_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "title": "MQTT Topic (e.g. home/livingroom/light/set)"},
                "payload": {"type": "string", "title": "Message Payload", "format": "textarea"}
            },
            "required": ["topic", "payload"]
        }
        
    def validate_config(self) -> bool:
        return bool(self.config.get("broker"))
        
    async def send(self, title: str, payload: str, parameters: Dict[str, Any], **kwargs) -> bool:
        broker = self.config.get("broker")
        port = int(self.config.get("port", 1883))
        username = self.config.get("username")
        password = self.config.get("password")
        
        topic = parameters.get("topic")
        msg_payload = parameters.get("payload", payload)
        
        if not broker or not topic:
            return False
            
        auth = None
        if username:
            auth = {'username': username, 'password': password or ''}
            
        try:
            publish.single(
                topic, 
                payload=msg_payload, 
                hostname=broker, 
                port=port, 
                auth=auth,
                client_id="keepmeupdated_mqtt"
            )
            return True
        except Exception as e:
            print(f"MQTT publish failed: {e}")
            return False
