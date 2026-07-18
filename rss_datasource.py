import feedparser
import asyncio
from typing import Dict, Any
from app.plugins.base import BaseDataSourcePlugin

class RSSDataSource(BaseDataSourcePlugin):
    
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
        
    @classmethod
    def get_context_schema(cls) -> list:
        return [
            {"name": "feed_title", "description": "Title of the RSS feed", "example": "Hacker News"},
            {"name": "title", "description": "Title of the latest entry", "example": "Show HN: KeepMeUpdated"},
            {"name": "link", "description": "URL of the latest entry", "example": "https://news.ycombinator.com"},
            {"name": "summary", "description": "Summary or description", "example": "A new platform..."}
        ]
        
    def validate_config(self) -> bool:
        return bool(self.config.get("feed_url"))
        
    async def fetch_context(self) -> Dict[str, Any]:
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
