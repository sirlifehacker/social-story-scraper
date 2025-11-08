# 🚀 Quick Start Guide

## What's Been Built

I've created a **production-ready backend** for your Social Story Scraper webapp! Here's what's ready to use:

### ✅ Completed Features

1. **FastAPI Backend** (Port 8000)
   - Complete REST API with authentication
   - Interactive API docs at `/api/v1/docs`
   - Secure JWT-based authentication
   - Rate limiting and CORS protection

2. **Multi-AI Provider Support**
   - Claude Sonnet 4.5 (Anthropic)
   - Gemini 2.5 Flash/Pro (Google)
   - GPT-4 Turbo / GPT-5 (OpenAI)
   - Switch models via settings API

3. **Database & Models**
   - PostgreSQL with full schema
   - User accounts with encrypted API keys
   - Scrape job tracking
   - Tweet, topic, and content idea storage

4. **Services**
   - Twitter/X scraping via Apify
   - AI analysis with your chosen model
   - Perplexity research integration
   - Telegram daily reports
   - Optional Notion sync
   - CSV export functionality

5. **Automation**
   - Daily scheduled scrapes (6:45 AM EDT default)
   - Timezone-aware scheduling
   - Background task processing

6. **Docker Deployment**
   - One-command startup: `docker-compose up`
   - PostgreSQL, Backend, Frontend containers
   - Auto-configured networking

---

## 🎯 Start Using It NOW

### Option 1: Docker (Easiest)

```bash
# Navigate to project
cd /home/user/social-story-scraper

# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**Access Points:**
- API Docs: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/health
- Frontend: http://localhost:3000 (when built)

### Option 2: Manual Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload --port 8000
```

---

## 🔑 First Time Setup

### 1. Register Your Account

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "YourSecurePassword123!"
  }'
```

### 2. Login & Get Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "YourSecurePassword123!"
  }'
```

Save the `access_token` from the response!

### 3. Add Your API Keys

```bash
# Replace YOUR_ACCESS_TOKEN with your token

# Add Apify
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"service_name": "apify", "api_key": "YOUR_APIFY_KEY"}'

# Add OpenAI (or anthropic/google_ai)
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"service_name": "openai", "api_key": "YOUR_OPENAI_KEY"}'

# Add Perplexity
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"service_name": "perplexity", "api_key": "YOUR_PERPLEXITY_KEY"}'

# Add Telegram (format: "bot_token|chat_id")
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"service_name": "telegram", "api_key": "BOT_TOKEN|CHAT_ID"}'
```

### 4. Configure Preferences

```bash
curl -X PUT "http://localhost:8000/api/v1/settings/preferences" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ai_model_provider": "openai",
    "ai_model_name": "gpt-4-turbo",
    "twitter_list_url": "https://x.com/i/lists/YOUR_LIST_ID",
    "daily_run_time": "06:45:00",
    "timezone": "America/New_York",
    "auto_run_enabled": true,
    "max_tweets_to_scrape": "50"
  }'
```

### 5. Run Your First Scrape!

```bash
curl -X POST "http://localhost:8000/api/v1/scrapes/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trigger_type": "manual"}'
```

This will:
1. Scrape tweets from your list
2. Analyze with AI
3. Research with Perplexity
4. Generate content ideas
5. Send Telegram notification
6. Save everything to database

### 6. View Results

```bash
# Get all scrape jobs
curl "http://localhost:8000/api/v1/scrapes/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get tweets from a job
curl "http://localhost:8000/api/v1/scrapes/{job_id}/tweets" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Export to CSV
curl "http://localhost:8000/api/v1/export/{job_id}/tweets" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -o tweets.csv
```

---

## 📱 Interactive API Documentation

Visit http://localhost:8000/api/v1/docs for a full interactive API explorer!

You can:
- Test all endpoints
- See request/response schemas
- Authenticate and try real requests
- Download OpenAPI spec

---

## 🤖 Setting Up Telegram Bot

1. Message `@BotFather` on Telegram
2. Send `/newbot` and follow prompts
3. Copy your bot token
4. Start a chat with your bot
5. Get your chat ID from: `https://api.telegram.org/bot<TOKEN>/getUpdates`
6. Add to app as: `bot_token|chat_id`

---

## 🎨 Switching AI Models

Want to try Claude or Gemini?

```bash
# Switch to Claude Sonnet 4.5
curl -X PUT "http://localhost:8000/api/v1/settings/preferences" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ai_model_provider": "anthropic",
    "ai_model_name": "claude-sonnet-4-5-20250929"
  }'

# Don't forget to add Anthropic API key!
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"service_name": "anthropic", "api_key": "YOUR_ANTHROPIC_KEY"}'
```

---

## 🔄 Daily Automated Runs

The scheduler starts automatically! It will:
- Run at your configured time (default 6:45 AM EDT)
- Use your selected AI model
- Send Telegram reports
- Save all data to database

Check scheduler status in backend logs:
```bash
docker-compose logs backend | grep -i "scheduled"
```

---

## 📊 What's Next?

### Immediate Next Steps:

1. **Test the Backend** ✓
   - Follow steps above to register, configure, and run a scrape
   - Verify Telegram notifications work
   - Export CSV and check data

2. **Build React Frontend** (Coming Soon)
   - Mobile-first dashboard
   - View scrape history
   - Browse tweets, topics, ideas
   - Configure settings via UI
   - Export data with one click

3. **Add Tests** (Recommended)
   - Unit tests for services
   - Integration tests for API
   - Security tests

### Future Enhancements:

- iOS mobile app
- Additional platform scrapers (Instagram, TikTok, LinkedIn)
- Advanced analytics dashboard
- Team collaboration
- A/B testing for content ideas

---

## 🆘 Need Help?

### Check Logs
```bash
docker-compose logs -f backend
docker-compose logs postgres
```

### Database Issues
```bash
# Restart database
docker-compose restart postgres

# Check if it's running
docker-compose ps postgres
```

### API Not Responding
```bash
# Restart backend
docker-compose restart backend

# Check health
curl http://localhost:8000/health
```

---

## 📝 Files Overview

```
social-story-scraper/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Auth & security
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Request/response schemas
│   │   ├── services/     # Business logic
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # DB setup
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # Database migrations
│   ├── .env              # Your secrets (DO NOT COMMIT)
│   ├── .env.example      # Template
│   ├── requirements.txt  # Dependencies
│   └── Dockerfile        # Container config
├── docker-compose.yml    # Multi-container setup
├── README.md             # Full documentation
└── QUICKSTART.md         # This file!
```

---

**You're all set! The backend is production-ready and waiting for you to build the frontend.** 🎉

For detailed API documentation, see README.md or visit http://localhost:8000/api/v1/docs
