"""Twitter/X Scraper Service using Apify"""
import httpx
from typing import Dict, Any, List
import asyncio


class ScraperService:
    """Service for scraping Twitter/X using Apify"""

    def __init__(self, apify_api_key: str):
        self.apify_api_key = apify_api_key
        self.base_url = "https://api.apify.com/v2"

    async def scrape_twitter_list(
        self,
        list_url: str,
        max_items: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Scrape tweets from a Twitter/X list using Apify

        Args:
            list_url: URL of the Twitter list to scrape
            max_items: Maximum number of tweets to fetch

        Returns:
            List of tweet data dictionaries
        """
        # Apify Twitter Scraper Actor ID
        actor_id = "apidojo/tweet-scraper"

        # Build request payload
        payload = {
            "customMapFunction": "(object) => { return {...object} }",
            "maxItems": max_items,
            "startUrls": [list_url]
        }

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                # Start the actor run
                run_response = await client.post(
                    f"{self.base_url}/acts/{actor_id}/runs",
                    params={"token": self.apify_api_key},
                    json=payload
                )
                run_response.raise_for_status()
                run_data = run_response.json()
                run_id = run_data["data"]["id"]

                # Wait for run to complete
                await self._wait_for_run(run_id, client)

                # Get dataset
                dataset_response = await client.get(
                    f"{self.base_url}/acts/{actor_id}/runs/{run_id}/dataset/items",
                    params={"token": self.apify_api_key}
                )
                dataset_response.raise_for_status()
                tweets = dataset_response.json()

                return self._process_tweets(tweets)

        except httpx.HTTPError as e:
            raise Exception(f"Apify scraping error: {str(e)}")

    async def _wait_for_run(self, run_id: str, client: httpx.AsyncClient, max_wait: int = 300):
        """Wait for Apify run to complete"""
        waited = 0
        while waited < max_wait:
            response = await client.get(
                f"{self.base_url}/actor-runs/{run_id}",
                params={"token": self.apify_api_key}
            )
            data = response.json()
            status = data["data"]["status"]

            if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
                if status != "SUCCEEDED":
                    raise Exception(f"Apify run failed with status: {status}")
                return

            await asyncio.sleep(5)
            waited += 5

        raise Exception("Apify run timed out")

    def _process_tweets(self, raw_tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and normalize tweet data from Apify"""
        processed = []

        for tweet in raw_tweets:
            try:
                processed.append({
                    "tweet_id": tweet.get("id") or tweet.get("id_str", ""),
                    "text": tweet.get("full_text") or tweet.get("text", ""),
                    "url": tweet.get("url", ""),
                    "author_username": tweet.get("author", {}).get("userName", ""),
                    "author_follower_count": tweet.get("author", {}).get("followers", 0),
                    "like_count": tweet.get("likeCount", 0),
                    "retweet_count": tweet.get("retweetCount", 0),
                    "reply_count": tweet.get("replyCount", 0),
                })
            except Exception as e:
                # Skip malformed tweets
                continue

        return processed

    def calculate_engagement_score(
        self,
        likes: int,
        retweets: int,
        replies: int,
        followers: int
    ) -> float:
        """Calculate engagement score for a tweet"""
        if followers == 0:
            return 0.0

        score = (likes + (2 * retweets) + (0.5 * replies)) / followers
        return round(score, 4)
