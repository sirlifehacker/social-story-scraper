# 🚀 Social Story Scraper - Full Stack WebApp

A production-ready, AI-powered social media story scraper that automatically identifies trending content, analyzes engagement patterns, and generates strategic content ideas. Built with FastAPI, React, and PostgreSQL.

## ✨ Features

- 🤖 **Multi-AI Provider Support**: Choose between Claude Sonnet 4.5, Gemini 2.5, or GPT-5 for analysis
- 🐦 **Twitter/X Scraping**: Automated scraping via Apify
- 📊 **AI-Powered Analysis**: Identifies top tweets and trending topics
- 🧠 **Deep Research**: Perplexity AI integration for topic insights
- 💡 **Content Idea Generation**: Viral content strategies based on trending data
- 📱 **Mobile-First UI**: Responsive design optimized for mobile usage
- 🔐 **Secure**: JWT authentication, encrypted API keys, security headers
- ⏰ **Automated Scheduling**: Daily runs at configured time (default: 6:45 AM EDT)
- 📨 **Telegram Reports**: Daily notifications with top insights
- 📥 **CSV Export**: Export all data for further analysis or Notion upload
- 🔄 **Optional Notion Integration**: Sync data to Notion databases

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         React Frontend (Port 3000)       │
│    Mobile-Responsive UI with Tailwind   │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│       FastAPI Backend (Port 8000)       │
│  ┌──────────────────────────────────┐  │
│  │ JWT Auth | Rate Limiting | CORS  │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │   Services:                       │  │
│  │   • Apify Twitter Scraper        │  │
│  │   • Multi-AI Analysis            │  │
│  │   • Perplexity Research          │  │
│  │   • Telegram Notifications       │  │
│  │   • APScheduler (Daily Runs)     │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│      PostgreSQL Database (Port 5432)    │
│   Users | API Keys | Jobs | Results    │
└─────────────────────────────────────────┘
```

---

## 📋 Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node.js 18+, PostgreSQL 15+

### Required API Keys

1. **Apify** - Twitter/X scraping ([Get key](https://console.apify.com/account/integrations))
2. **AI Provider** (choose one or more):
   - **OpenAI** ([Get key](https://platform.openai.com/api-keys))
   - **Anthropic** ([Get key](https://console.anthropic.com/))
   - **Google AI** ([Get key](https://makersuite.google.com/app/apikey))
3. **Perplexity AI** ([Get key](https://www.perplexity.ai/settings/api))
4. **Telegram Bot** ([Create bot](https://t.me/botfather))
5. **Notion** (Optional) ([Get key](https://www.notion.so/my-integrations))

---

## 🚀 Quick Start with Docker (Recommended)

### 1. Clone and Setup

```bash
cd social-story-scraper
cp backend/.env.example backend/.env
```

### 2. Configure Environment Variables

Edit `backend/.env` and add your credentials:

```bash
# Generate secure keys (run these commands):
python -c "import secrets; print(secrets.token_urlsafe(32))"  # For SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"  # For ENCRYPTION_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"  # For JWT_SECRET_KEY

# Database (leave as-is for Docker)
DATABASE_URL=postgresql://scraper_user:scraper_password@postgres:5432/social_scraper_db

# Security Keys (paste generated keys)
SECRET_KEY=<your-generated-secret-key>
ENCRYPTION_KEY=<your-generated-encryption-key>
JWT_SECRET_KEY=<your-generated-jwt-key>

# Scheduling
TIMEZONE=America/New_York
DAILY_RUN_TIME=06:45

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### 3. Start the Application

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- FastAPI backend (port 8000)
- React frontend (port 3000) - *Coming soon*

### 4. Access the Application

- **API Documentation**: http://localhost:8000/api/v1/docs
- **Backend Health**: http://localhost:8000/health
- **Frontend**: http://localhost:3000 *(in development)*

---

## 🔧 Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Initialize database
alembic upgrade head

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup (Coming Soon)

```bash
cd frontend
npm install
npm start
```

---

## 📖 API Usage Guide

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

Response includes `access_token` - use this in subsequent requests.

### 3. Configure API Keys

```bash
# Add Apify key
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "apify",
    "api_key": "apify_api_xxx"
  }'

# Add OpenAI key
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "openai",
    "api_key": "sk-xxx"
  }'

# Add Perplexity key
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "perplexity",
    "api_key": "pplx-xxx"
  }'

# Add Telegram (format: "bot_token|chat_id")
curl -X POST "http://localhost:8000/api/v1/settings/api-keys" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "telegram",
    "api_key": "123456:ABC-DEF|123456789"
  }'
```

### 4. Configure Preferences

```bash
curl -X PUT "http://localhost:8000/api/v1/settings/preferences" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ai_model_provider": "openai",
    "ai_model_name": "gpt-4-turbo",
    "twitter_list_url": "https://x.com/i/lists/1944053485882028279",
    "daily_run_time": "06:45:00",
    "timezone": "America/New_York",
    "auto_run_enabled": true,
    "max_tweets_to_scrape": "50"
  }'
```

### 5. Trigger Manual Scrape

```bash
curl -X POST "http://localhost:8000/api/v1/scrapes/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trigger_type": "manual"
  }'
```

### 6. View Results

```bash
# Get all scrape jobs
curl "http://localhost:8000/api/v1/scrapes/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get specific job details
curl "http://localhost:8000/api/v1/scrapes/{job_id}" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Get tweets from job
curl "http://localhost:8000/api/v1/scrapes/{job_id}/tweets" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Export to CSV
curl "http://localhost:8000/api/v1/export/{job_id}/tweets" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -o tweets.csv
```

---

## 🤖 Setting Up Telegram Bot

### 1. Create Bot with BotFather

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to create your bot
4. Copy the **bot token** (format: `123456:ABC-DEF...`)

### 2. Get Your Chat ID

1. Start a chat with your new bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for `"chat":{"id":123456789}` - that's your chat ID

### 3. Add to App

Format for API key: `bot_token|chat_id`

Example: `123456:ABC-DEF|123456789`

---

## 🎨 AI Model Selection

### Supported Models

| Provider | Model | Best For | Cost (per 1M tokens) |
|----------|-------|----------|---------------------|
| **Anthropic** | claude-sonnet-4-5 | Nuanced analysis, detailed content | ~$3-$15 |
| **Google** | gemini-2.5-flash | Fast, cost-effective | ~$0.10-$0.30 |
| **Google** | gemini-2.5-pro | Balanced quality/cost | ~$1.25-$5 |
| **OpenAI** | gpt-4-turbo | Reliable, proven | ~$2.50-$10 |
| **OpenAI** | gpt-5 | Latest OpenAI model | TBD |

### Switching Models

Update your preferences via API or UI (when available):

```json
{
  "ai_model_provider": "anthropic",
  "ai_model_name": "claude-sonnet-4-5-20250929"
}
```

---

## 📅 Automated Scheduling

The scheduler automatically runs scrapes based on your preferences:

- **Default Time**: 6:45 AM EDT
- **Configurable**: Change via preferences endpoint
- **Timezone-Aware**: Supports any timezone (e.g., "America/New_York", "Europe/London", "Asia/Tokyo")

The scheduler starts automatically with the backend application.

---

## 🔒 Security Features

- ✅ JWT-based authentication with refresh tokens
- ✅ Password hashing with bcrypt
- ✅ API key encryption (Fernet symmetric encryption)
- ✅ Rate limiting on endpoints
- ✅ CORS configuration
- ✅ Security headers (CSP, X-Frame-Options, etc.)
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS prevention

---

## 📊 Database Schema

<details>
<summary>Click to expand database structure</summary>

- **users**: User accounts
- **api_keys**: Encrypted API credentials
- **user_preferences**: AI model and scheduling preferences
- **scrape_jobs**: Scraping job history and status
- **tweets**: Scraped tweet data
- **trending_topics**: Identified trending topics
- **content_ideas**: AI-generated content strategies

</details>

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest --cov=app tests/
```

### Security Scanning

```bash
# Check for security vulnerabilities
bandit -r app/

# Check dependencies
safety check
```

---

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
docker-compose logs backend
```

### API Key Errors

- Ensure all required API keys are configured
- Check API key format (especially Telegram: `token|chat_id`)
- Verify API keys have proper permissions

### Scraping Fails

- Check Apify account credits
- Verify Twitter list URL is public
- Check backend logs: `docker-compose logs backend`

---

## 📝 Development Roadmap

- [x] Backend API with FastAPI
- [x] Multi-AI provider support
- [x] Authentication & authorization
- [x] Database models & migrations
- [x] Scraping service (Apify)
- [x] AI analysis services
- [x] Telegram notifications
- [x] CSV export
- [x] Automated scheduling
- [x] Docker deployment
- [ ] React frontend UI
- [ ] Mobile app (iOS)
- [ ] Additional platform scrapers (Instagram, TikTok, LinkedIn)
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] A/B testing for content ideas

---

## 🤝 Contributing

This is a personal project. Feel free to fork and customize for your own use!

---

## 📄 License

MIT License - Feel free to use and modify for your needs.

---

## 🙏 Acknowledgments

- Based on the N8N automation workflow
- Built with FastAPI, React, PostgreSQL
- AI powered by OpenAI, Anthropic, and Google
- Scraping via Apify
- Research via Perplexity AI

---

## 📞 Support

For issues or questions:
1. Check the API documentation: http://localhost:8000/api/v1/docs
2. Review logs: `docker-compose logs`
3. Verify environment variables in `.env`

---

**Happy Scraping! 🚀**
