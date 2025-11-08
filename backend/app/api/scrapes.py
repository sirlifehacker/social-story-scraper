"""Scrape job routes"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import asyncio
from ..database import get_db
from ..models.user import User
from ..models.scrape_job import ScrapeJob, JobStatus
from ..models.tweet import Tweet
from ..models.trending_topic import TrendingTopic
from ..models.content_idea import ContentIdea
from ..schemas.scrape_job import ScrapeJobCreate, ScrapeJobResponse
from ..schemas.tweet import TweetResponse
from ..schemas.trending_topic import TrendingTopicResponse
from ..schemas.content_idea import ContentIdeaResponse
from ..core.deps import get_current_active_user
from ..services.scrape_orchestrator import ScrapeOrchestrator

router = APIRouter(prefix="/scrapes", tags=["Scrapes"])


async def execute_scrape_background(job_id: UUID, user_id: UUID):
    """Background task to execute scraping"""
    from ..database import SessionLocal
    db = SessionLocal()
    try:
        orchestrator = ScrapeOrchestrator(db)
        await orchestrator.execute_scrape(job_id, user_id)
    finally:
        db.close()


@router.post("/", response_model=ScrapeJobResponse, status_code=status.HTTP_201_CREATED)
async def create_scrape_job(
    scrape_data: ScrapeJobCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create and execute a new scrape job"""
    # Create scrape job
    scrape_job = ScrapeJob(
        user_id=current_user.id,
        trigger_type=scrape_data.trigger_type,
        status=JobStatus.PENDING
    )
    db.add(scrape_job)
    db.commit()
    db.refresh(scrape_job)

    # Add background task to execute scraping
    background_tasks.add_task(execute_scrape_background, scrape_job.id, current_user.id)

    return scrape_job


@router.get("/", response_model=List[ScrapeJobResponse])
async def get_scrape_jobs(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all scrape jobs for current user"""
    jobs = db.query(ScrapeJob).filter(
        ScrapeJob.user_id == current_user.id
    ).order_by(ScrapeJob.created_at.desc()).offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=ScrapeJobResponse)
async def get_scrape_job(
    job_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific scrape job"""
    job = db.query(ScrapeJob).filter(
        ScrapeJob.id == job_id,
        ScrapeJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scrape job not found"
        )

    return job


@router.get("/{job_id}/tweets", response_model=List[TweetResponse])
async def get_job_tweets(
    job_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all tweets from a specific scrape job"""
    # Verify job belongs to user
    job = db.query(ScrapeJob).filter(
        ScrapeJob.id == job_id,
        ScrapeJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scrape job not found"
        )

    tweets = db.query(Tweet).filter(Tweet.scrape_job_id == job_id).order_by(
        Tweet.engagement_score.desc()
    ).all()
    return tweets


@router.get("/{job_id}/topics", response_model=List[TrendingTopicResponse])
async def get_job_topics(
    job_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all trending topics from a specific scrape job"""
    # Verify job belongs to user
    job = db.query(ScrapeJob).filter(
        ScrapeJob.id == job_id,
        ScrapeJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scrape job not found"
        )

    topics = db.query(TrendingTopic).filter(
        TrendingTopic.scrape_job_id == job_id
    ).order_by(TrendingTopic.rank).all()
    return topics


@router.get("/{job_id}/ideas", response_model=List[ContentIdeaResponse])
async def get_job_ideas(
    job_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all content ideas from a specific scrape job"""
    # Verify job belongs to user
    job = db.query(ScrapeJob).filter(
        ScrapeJob.id == job_id,
        ScrapeJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scrape job not found"
        )

    ideas = db.query(ContentIdea).filter(
        ContentIdea.scrape_job_id == job_id
    ).all()
    return ideas
