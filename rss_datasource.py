import feedparser
import asyncio
from typing import Dict, Any
from app.plugins.base import BaseDataSource

class RSSDataSource(BaseDataSource):
    
    @classmethod
    def get_plugin_id(cls) -> str:
        return "rss_feed"
        
    @classmethod
    def get_name(cls) -> str:
        return "RSS / News Fetcher"
        
    @classmethod
    def get_config_schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "feed_url": {"type": "string", "title": "RSS Feed URL (e.g. https://news.ycombinator.com/rss)"}
            },
            "required": ["feed_url"]
        }
        
    def validate_config(self) -> bool:
        return bool(self.config.get("feed_url"))
        
    async def fetch_data(self) -> Dict[str, Any]:
        feed_url = self.config.get("feed_url")
        
        if not feed_url:
            return {"feed_title": "Error", "title": "Error", "link": "Error", "summary": "Error"}
            
        try:
            loop = asyncio.get_event_loop()
            feed = await loop.run_in_executor(None, feedparser.parse, feed_url)
            
            if feed.entries:
                latest = feed.entries[0]
                return {
                    "feed_title": getattr(feed.feed, "title", "Unknown Feed"),
                    "title": getattr(latest, "title", "No Title"),
                    "link": getattr(latest, "link", ""),
                    "summary": getattr(latest, "summary", getattr(latest, "description", ""))
                }
        except Exception as e:
            print(f"RSS fetch failed: {e}")
            
        return {"feed_title": "Error", "title": "Error", "link": "Error", "summary": "Error"}
