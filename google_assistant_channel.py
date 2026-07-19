import urllib.parse
from typing import Dict, Any
from .base import BaseNotificationChannel

try:
    import pychromecast
except ImportError:
    pychromecast = None

class GoogleAssistantChannel(BaseNotificationChannel):
    
    @classmethod
    def get_plugin_id(cls) -> str:
        return "google_assistant"
        
    @classmethod
    def get_name(cls) -> str:
        return "Google Assistant (Cast)"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string", 
                    "title": "Device Name", 
                    "description": "The exact name of your Google Nest device (e.g. 'Living Room speaker')",
                    "dynamic_options": True
                },
                "language": {
                    "type": "string",
                    "title": "Language Code",
                    "description": "The language code for text-to-speech (e.g. 'en', 'el', 'fr')",
                    "default": "en"
                }
            },
            "required": ["device_name"]
        }
        
    @classmethod
    def get_notification_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string", "title": "Message to speak", "format": "textarea"}
            },
            "required": ["message"]
        }
        
    @classmethod
    async def get_dynamic_options(cls, field_name: str) -> list:
        if field_name == "device_name":
            if pychromecast is None:
                return []
            try:
                chromecasts, browser = pychromecast.get_chromecasts()
                pychromecast.discovery.stop_discovery(browser)
                return [c.cast_info.friendly_name for c in chromecasts]
            except Exception as e:
                print(f"Error discovering chromecasts: {e}")
                return []
        return []
        
    def validate_config(self) -> bool:
        return bool(self.config.get("device_name"))
        
    async def send(self, title: str, payload: str, parameters: Dict[str, Any], **kwargs) -> bool:
        if pychromecast is None:
            print("Google Assistant plugin requires 'pychromecast'. Please install it.")
            return False

        device_name = self.config.get("device_name", "").strip()
        lang = self.config.get("language", "en").strip()
        
        if not device_name:
            return False
            
        message = parameters.get("message") or payload
        if not message:
            return False
            
        # Build the Google Translate TTS URL
        encoded_message = urllib.parse.quote(message)
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&total=1&idx=0&client=tw-ob&q={encoded_message}&tl={lang}"
        
        try:
            import ipaddress
            is_ip = False
            try:
                ipaddress.ip_address(device_name)
                is_ip = True
            except ValueError:
                pass
                
            if is_ip:
                cast = pychromecast.get_chromecast_from_host(
                    (device_name, 8009, None, None, None),
                    tries=1,
                    timeout=5.0
                )
                if not cast:
                    print(f"Could not connect to Google Cast device at IP '{device_name}'.")
                    return False
                cast.wait(timeout=5.0)
                if not cast.is_idle:
                    print(f"Timed out waiting for cast device at IP '{device_name}'.")
                    return False
                browser = None
            else:
                # Discover chromecasts matching the device name
                chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device_name])
                if not chromecasts:
                    print(f"Could not find a Google Cast device named '{device_name}' on the local network.")
                    return False
                    
                cast = chromecasts[0]
                cast.wait(timeout=5.0)
            
            # Stop any currently playing media/app to ensure the notification is heard
            cast.quit_app()
            import time
            time.sleep(1) # Give it a brief moment to exit the current app
            
            # Play the generated TTS URL
            cast.media_controller.play_media(tts_url, "audio/mp3")
            cast.media_controller.block_until_active()
            
            import time
            # Wait for the media to start playing or buffering
            for _ in range(50):
                if cast.media_controller.status.player_state in ['PLAYING', 'BUFFERING']:
                    break
                time.sleep(0.1)
                
            # Wait for the media to finish playing
            for _ in range(60): # Max 30 seconds
                if cast.media_controller.status.player_state not in ['PLAYING', 'BUFFERING']:
                    break
                time.sleep(0.5)
            
            # Clean up the discovery browser
            if browser:
                pychromecast.discovery.stop_discovery(browser)
                
            # Stop the Default Media Receiver to release the device back to its idle state
            cast.quit_app()
            time.sleep(1) # Give it a moment to process the quit command
                
            # Explicitly disconnect to free up the socket for future notifications
            cast.disconnect()
            return True
            
        except Exception as e:
            print(f"Google Assistant send failed: {e}")
            return False
