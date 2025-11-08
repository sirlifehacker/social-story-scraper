"""Notion Integration Service (Optional)"""
from notion_client import Client
from typing import List, Dict, Any


class NotionService:
    """Service for uploading data to Notion databases"""

    def __init__(self, api_key: str):
        self.client = Client(auth=api_key)

    async def upload_tweets(
        self,
        database_id: str,
        tweets: List[Dict[str, Any]]
    ):
        """Upload tweets to Notion database"""
        for tweet in tweets:
            try:
                self.client.pages.create(
                    parent={"database_id": database_id},
                    properties={
                        "Tweet ID": {
                            "title": [
                                {
                                    "text": {"content": tweet.get('tweet_id', '')}
                                }
                            ]
                        },
                        "Tweet Text": {
                            "rich_text": [
                                {
                                    "text": {"content": tweet.get('text', '')[:2000]}
                                }
                            ]
                        },
                        "Tweet URL": {
                            "url": tweet.get('url', '')
                        },
                        "Like Count": {
                            "number": tweet.get('like_count', 0)
                        },
                        "Engagement Score": {
                            "number": tweet.get('engagement_score', 0.0)
                        }
                    }
                )
            except Exception as e:
                # Log error but continue with other tweets
                print(f"Failed to upload tweet {tweet.get('tweet_id')}: {str(e)}")

    async def upload_topics(
        self,
        database_id: str,
        topics: List[Dict[str, Any]]
    ):
        """Upload trending topics to Notion database"""
        for topic in topics:
            try:
                self.client.pages.create(
                    parent={"database_id": database_id},
                    properties={
                        "Topic": {
                            "title": [
                                {
                                    "text": {"content": topic.get('title', '')}
                                }
                            ]
                        },
                        "Description": {
                            "rich_text": [
                                {
                                    "text": {"content": topic.get('description', '')[:2000]}
                                }
                            ]
                        },
                        "Key Insights": {
                            "rich_text": [
                                {
                                    "text": {"content": topic.get('key_insights', '')[:2000]}
                                }
                            ]
                        },
                        "Visual Analogy": {
                            "rich_text": [
                                {
                                    "text": {"content": topic.get('visual_analogy', '')[:2000]}
                                }
                            ]
                        }
                    }
                )
            except Exception as e:
                print(f"Failed to upload topic {topic.get('title')}: {str(e)}")

    async def upload_content_ideas(
        self,
        database_id: str,
        ideas: List[Dict[str, Any]]
    ):
        """Upload content ideas to Notion database"""
        for idea in ideas:
            try:
                self.client.pages.create(
                    parent={"database_id": database_id},
                    properties={
                        "Title": {
                            "title": [
                                {
                                    "text": {"content": idea.get('title', '')}
                                }
                            ]
                        },
                        "Content Overview": {
                            "rich_text": [
                                {
                                    "text": {"content": idea.get('content_overview', '')[:2000]}
                                }
                            ]
                        },
                        "Target Audience": {
                            "rich_text": [
                                {
                                    "text": {"content": idea.get('target_audience', '')[:2000]}
                                }
                            ]
                        },
                        "Core Pain Point": {
                            "rich_text": [
                                {
                                    "text": {"content": idea.get('core_pain_point', '')[:2000]}
                                }
                            ]
                        }
                    }
                )
            except Exception as e:
                print(f"Failed to upload idea {idea.get('title')}: {str(e)}")
