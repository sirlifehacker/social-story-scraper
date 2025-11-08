"""Scheduler Service for automated daily scraping"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import time
import pytz
from typing import Callable
import logging

logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for scheduling automated scraping jobs"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.jobs = {}

    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")

    def schedule_daily_scrape(
        self,
        user_id: str,
        scrape_function: Callable,
        run_time: time,
        timezone_str: str = "America/New_York"
    ):
        """
        Schedule a daily scraping job for a user

        Args:
            user_id: User identifier
            scrape_function: Async function to execute
            run_time: Time to run (datetime.time object)
            timezone_str: Timezone string (e.g., 'America/New_York')
        """
        job_id = f"daily_scrape_{user_id}"

        # Remove existing job if present
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)

        # Create timezone-aware trigger
        tz = pytz.timezone(timezone_str)
        trigger = CronTrigger(
            hour=run_time.hour,
            minute=run_time.minute,
            timezone=tz
        )

        # Add job
        job = self.scheduler.add_job(
            scrape_function,
            trigger=trigger,
            id=job_id,
            name=f"Daily scrape for user {user_id}",
            replace_existing=True
        )

        self.jobs[job_id] = job
        logger.info(
            f"Scheduled daily scrape for user {user_id} at "
            f"{run_time.strftime('%H:%M')} {timezone_str}"
        )

    def remove_user_schedule(self, user_id: str):
        """Remove scheduled job for a user"""
        job_id = f"daily_scrape_{user_id}"
        if job_id in self.jobs:
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]
            logger.info(f"Removed scheduled scrape for user {user_id}")

    def get_next_run_time(self, user_id: str):
        """Get next scheduled run time for a user"""
        job_id = f"daily_scrape_{user_id}"
        if job_id in self.jobs:
            job = self.scheduler.get_job(job_id)
            if job:
                return job.next_run_time
        return None


# Global scheduler instance
scheduler_service = SchedulerService()
