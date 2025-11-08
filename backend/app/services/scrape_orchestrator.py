"""Scrape Orchestrator - Coordinates all scraping and analysis services"""
from sqlalchemy.orm import Session
from typing import Dict, Any
from uuid import UUID
import logging
from datetime import datetime

from ..models.scrape_job import ScrapeJob, JobStatus, TriggerType
from ..models.tweet import Tweet
from ..models.trending_topic import TrendingTopic
from ..models.content_idea import ContentIdea
from ..models.user import User
from ..models.user_preferences import UserPreferences
from ..models.api_key import APIKey, ServiceName
from ..core.security import decrypt_api_key
from .scraper_service import ScraperService
from .ai_service import AIAnalysisService
from .perplexity_service import PerplexityService
from .telegram_service import TelegramService

logger = logging.getLogger(__name__)


class ScrapeOrchestrator:
    """Orchestrates the complete scraping and analysis workflow"""

    def __init__(self, db: Session):
        self.db = db

    async def execute_scrape(self, job_id: UUID, user_id: UUID):
        """
        Execute complete scraping workflow

        Steps:
        1. Get user preferences and API keys
        2. Scrape Twitter/X
        3. Analyze with AI
        4. Research with Perplexity
        5. Generate content ideas
        6. Save to database
        7. Send Telegram notification
        8. (Optional) Upload to Notion
        """
        job = self.db.query(ScrapeJob).filter(ScrapeJob.id == job_id).first()
        if not job:
            raise Exception(f"Scrape job {job_id} not found")

        try:
            # Update job status
            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()
            self.db.commit()

            # Step 1: Get user configuration
            preferences = self.db.query(UserPreferences).filter(
                UserPreferences.user_id == user_id
            ).first()

            api_keys = self._get_api_keys(user_id)

            # Step 2: Scrape Twitter
            logger.info(f"Starting Twitter scrape for job {job_id}")
            scraper = ScraperService(api_keys[ServiceName.APIFY])
            tweets_data = await scraper.scrape_twitter_list(
                preferences.twitter_list_url,
                max_items=int(preferences.max_tweets_to_scrape)
            )

            # Calculate engagement scores
            for tweet in tweets_data:
                tweet['engagement_score'] = scraper.calculate_engagement_score(
                    tweet['like_count'],
                    tweet['retweet_count'],
                    tweet['reply_count'],
                    tweet['author_follower_count']
                )

            # Step 3: AI Analysis
            logger.info(f"Analyzing tweets with {preferences.ai_model_provider}")
            ai_service = AIAnalysisService(
                preferences.ai_model_provider,
                preferences.ai_model_name,
                api_keys[self._get_ai_service_name(preferences.ai_model_provider)]
            )

            analysis_result = await ai_service.analyze_tweets(tweets_data)

            # Step 4: Perplexity Research
            logger.info("Conducting Perplexity research")
            perplexity_service = PerplexityService(api_keys[ServiceName.PERPLEXITY])
            research_text = await perplexity_service.research_topics(
                analysis_result.get('trending_topics', [])
            )

            # Step 5: Generate Content Ideas
            logger.info("Generating content ideas")
            content_result = await ai_service.generate_content_ideas(
                analysis_result,
                research_text
            )

            # Step 6: Save to database
            logger.info("Saving results to database")
            await self._save_results(
                job_id,
                analysis_result,
                research_text,
                content_result
            )

            # Update job
            job.ai_model_used = f"{preferences.ai_model_provider}:{preferences.ai_model_name}"
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            job.metadata = {
                "tweets_scraped": len(tweets_data),
                "topics_found": len(analysis_result.get('trending_topics', [])),
                "ideas_generated": len(content_result.get('content_ideas', []))
            }
            self.db.commit()

            # Step 7: Send Telegram notification
            if ServiceName.TELEGRAM in api_keys:
                logger.info("Sending Telegram notification")
                try:
                    telegram_service = TelegramService(
                        api_keys[ServiceName.TELEGRAM],
                        self._get_telegram_chat_id(user_id)
                    )
                    await telegram_service.send_daily_report(
                        str(job_id),
                        analysis_result.get('top_tweets', []),
                        analysis_result.get('trending_topics', []),
                        content_result.get('content_ideas', [])
                    )
                except Exception as e:
                    logger.error(f"Telegram notification failed: {str(e)}")

            logger.info(f"Scrape job {job_id} completed successfully")

        except Exception as e:
            logger.error(f"Scrape job {job_id} failed: {str(e)}")
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            self.db.commit()

            # Try to send error notification
            if ServiceName.TELEGRAM in api_keys:
                try:
                    telegram_service = TelegramService(
                        api_keys[ServiceName.TELEGRAM],
                        self._get_telegram_chat_id(user_id)
                    )
                    await telegram_service.send_error_notification(str(e))
                except:
                    pass

            raise

    def _get_api_keys(self, user_id: UUID) -> Dict[ServiceName, str]:
        """Get and decrypt all API keys for user"""
        api_keys_db = self.db.query(APIKey).filter(
            APIKey.user_id == user_id,
            APIKey.is_active == True
        ).all()

        api_keys = {}
        for key in api_keys_db:
            try:
                api_keys[key.service_name] = decrypt_api_key(key.encrypted_key)
            except Exception as e:
                logger.error(f"Failed to decrypt {key.service_name} API key: {str(e)}")

        return api_keys

    def _get_ai_service_name(self, provider) -> ServiceName:
        """Map AI provider to service name"""
        from ..models.user_preferences import AIProvider

        mapping = {
            AIProvider.OPENAI: ServiceName.OPENAI,
            AIProvider.ANTHROPIC: ServiceName.ANTHROPIC,
            AIProvider.GOOGLE: ServiceName.GOOGLE_AI
        }
        return mapping.get(provider, ServiceName.OPENAI)

    def _get_telegram_chat_id(self, user_id: UUID) -> str:
        """Get Telegram chat ID from API key metadata"""
        # For simplicity, we'll store chat_id as part of the encrypted key
        # Format: "bot_token|chat_id"
        telegram_key = self.db.query(APIKey).filter(
            APIKey.user_id == user_id,
            APIKey.service_name == ServiceName.TELEGRAM
        ).first()

        if telegram_key:
            decrypted = decrypt_api_key(telegram_key.encrypted_key)
            if '|' in decrypted:
                _, chat_id = decrypted.split('|', 1)
                return chat_id

        return ""

    async def _save_results(
        self,
        job_id: UUID,
        analysis_result: Dict[str, Any],
        research_text: str,
        content_result: Dict[str, Any]
    ):
        """Save scraping results to database"""
        # Save tweets
        for tweet_data in analysis_result.get('top_tweets', []):
            tweet = Tweet(
                scrape_job_id=job_id,
                tweet_id=tweet_data.get('tweet_id'),
                text=tweet_data.get('text'),
                url=tweet_data.get('url'),
                author_username=tweet_data.get('author_username'),
                author_follower_count=tweet_data.get('author_follower_count'),
                like_count=tweet_data.get('like_count', 0),
                retweet_count=tweet_data.get('retweet_count', 0),
                reply_count=tweet_data.get('reply_count', 0),
                engagement_score=tweet_data.get('engagement_score', 0.0)
            )
            self.db.add(tweet)

        # Save trending topics
        for topic_data in analysis_result.get('trending_topics', []):
            topic = TrendingTopic(
                scrape_job_id=job_id,
                rank=topic_data.get('rank', 0),
                title=topic_data.get('title'),
                description=topic_data.get('description'),
                key_insights=research_text  # Simplified - should parse per topic
            )
            self.db.add(topic)

        # Save content ideas
        for idea_data in content_result.get('content_ideas', []):
            idea = ContentIdea(
                scrape_job_id=job_id,
                title=idea_data.get('title'),
                content_overview=idea_data.get('content_overview'),
                target_audience=idea_data.get('target_audience'),
                core_pain_point=idea_data.get('core_pain_point'),
                hook_strategy=idea_data.get('hook_strategy'),
                storyline_outline=idea_data.get('storyline_outline')
            )
            self.db.add(idea)

        self.db.commit()
