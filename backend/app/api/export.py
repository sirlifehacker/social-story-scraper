"""Export routes for CSV downloads"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import io
import csv
from ..database import get_db
from ..models.user import User
from ..models.scrape_job import ScrapeJob
from ..models.tweet import Tweet
from ..models.trending_topic import TrendingTopic
from ..models.content_idea import ContentIdea
from ..core.deps import get_current_active_user

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/{job_id}/tweets")
async def export_tweets_csv(
    job_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export tweets to CSV"""
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

    tweets = db.query(Tweet).filter(Tweet.scrape_job_id == job_id).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'Tweet ID', 'Text', 'URL', 'Author', 'Followers',
        'Likes', 'Retweets', 'Replies', 'Engagement Score', 'Created At'
    ])

    # Write data
    for tweet in tweets:
        writer.writerow([
            tweet.tweet_id,
            tweet.text,
            tweet.url,
            tweet.author_username or '',
            tweet.author_follower_count or 0,
            tweet.like_count,
            tweet.retweet_count,
            tweet.reply_count,
            tweet.engagement_score,
            tweet.created_at.isoformat()
        ])

    # Create response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=tweets_{job_id}.csv"
        }
    )


@router.get("/{job_id}/topics")
async def export_topics_csv(
    job_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export trending topics to CSV"""
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

    topics = db.query(TrendingTopic).filter(TrendingTopic.scrape_job_id == job_id).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'Rank', 'Title', 'Description', 'Key Insights',
        'Visual Analogy', 'Most Benefited Niches', 'Created At'
    ])

    # Write data
    for topic in topics:
        writer.writerow([
            topic.rank,
            topic.title,
            topic.description,
            topic.key_insights or '',
            topic.visual_analogy or '',
            topic.most_benefited_niches or '',
            topic.created_at.isoformat()
        ])

    # Create response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=topics_{job_id}.csv"
        }
    )


@router.get("/{job_id}/ideas")
async def export_ideas_csv(
    job_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export content ideas to CSV"""
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

    ideas = db.query(ContentIdea).filter(ContentIdea.scrape_job_id == job_id).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'Title', 'Content Overview', 'Target Audience',
        'Core Pain Point', 'Created At'
    ])

    # Write data
    for idea in ideas:
        writer.writerow([
            idea.title,
            idea.content_overview,
            idea.target_audience or '',
            idea.core_pain_point or '',
            idea.created_at.isoformat()
        ])

    # Create response
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=ideas_{job_id}.csv"
        }
    )
