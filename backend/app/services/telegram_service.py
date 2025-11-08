"""Telegram Notification Service"""
from telegram import Bot
from typing import Dict, Any, List
import asyncio


class TelegramService:
    """Service for sending Telegram notifications"""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    async def send_daily_report(
        self,
        scrape_job_id: str,
        top_tweets: List[Dict[str, Any]],
        trending_topics: List[Dict[str, Any]],
        content_ideas: List[Dict[str, Any]],
        webapp_url: str = "http://localhost:3000"
    ):
        """Send daily scraping report via Telegram"""
        message = self._format_report(
            scrape_job_id,
            top_tweets,
            trending_topics,
            content_ideas,
            webapp_url
        )

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        except Exception as e:
            raise Exception(f"Telegram send error: {str(e)}")

    def _format_report(
        self,
        scrape_job_id: str,
        top_tweets: List[Dict[str, Any]],
        trending_topics: List[Dict[str, Any]],
        content_ideas: List[Dict[str, Any]],
        webapp_url: str
    ) -> str:
        """Format the daily report message"""
        message = f"""
📊 <b>Daily Social Story Report</b>
━━━━━━━━━━━━━━━━━━━━

<b>🐦 Top Tweets ({len(top_tweets)})</b>
"""

        # Add top 3 tweets
        for i, tweet in enumerate(top_tweets[:3], 1):
            message += f"""
{i}. {tweet.get('text', '')[:100]}...
   💙 {tweet.get('like_count', 0)} | 📊 Score: {tweet.get('engagement_score', 0)}
   🔗 <a href="{tweet.get('url', '')}">View Tweet</a>
"""

        message += f"""
━━━━━━━━━━━━━━━━━━━━

<b>📈 Trending Topics ({len(trending_topics)})</b>
"""

        # Add top 3 topics
        for i, topic in enumerate(trending_topics[:3], 1):
            message += f"""
{i}. <b>{topic.get('title', '')}</b>
   {topic.get('description', '')[:150]}...
"""

        message += f"""
━━━━━━━━━━━━━━━━━━━━

<b>💡 Content Ideas Generated: {len(content_ideas)}</b>

<b>🔗 View Full Report:</b>
{webapp_url}/scrapes/{scrape_job_id}

━━━━━━━━━━━━━━━━━━━━
"""

        return message

    async def send_error_notification(self, error_message: str):
        """Send error notification"""
        message = f"""
❌ <b>Scraping Error</b>

{error_message}

Please check your API keys and configuration in the webapp.
"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="HTML"
            )
        except Exception as e:
            # Log error but don't raise - error notification failure shouldn't crash
            print(f"Failed to send error notification: {str(e)}")

    async def test_connection(self) -> bool:
        """Test Telegram connection"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text="✅ Telegram connection successful! Social Story Scraper is connected."
            )
            return True
        except Exception as e:
            raise Exception(f"Telegram connection test failed: {str(e)}")
