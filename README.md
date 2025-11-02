# 🧠 Social Story Scraper  
### A series of N8N automations for sniping early trending stories on X (Twitter) and turning them into viral content ideas

---

## ▶️ Video Walkthrough

[Linked here](https://youtu.be/HidLFnkrAj4) is a FULL DEMO with output examples and a step by step video walkthrough of how to setup the automation.

## ⚡ Overview

**Social Story Scraper** is an AI-powered automation built in n8n that automatically:
- Scrapes early trending tweets from X Lists or keywords  
- Analyzes them for engagement and trending themes  
- Runs deep research on each topic with **Perplexity AI**  
- Generates elite content ideas using **GPT-4 / GPT-5** via **OpenRouter**  
- Sends you a beautiful HTML email digest of daily AI stories  
- Uploads all data automatically to **Notion databases**

It’s designed for creators, strategists, and media operators who want to **spot viral trends early** and **turn them into content that blows up**.

---

## 🧩 Features

| Feature | Description |
|----------|-------------|
| 🐦 **X Scraper** | Pulls top 50–100 tweets from any X List (via Apify). Calculates engagement scores and trending topics. |
| 🔍 **AI Topic Analyzer** | Uses GPT to identify recurring themes, emerging ideas, and conversation sentiment. |
| 🧠 **Perplexity Researcher** | Expands the top 5 trending topics with credible web insights and visual analogies. |
| 🎨 **Content Strategist** | Generates 5 fully-structured viral content ideas with hooks, visual cues, and storylines (based on Callaway’s framework). |
| 🗂 **Notion Integration** | Auto-uploads tweets, insights, and ideas into three connected Notion databases: `Twitter Stories`, `AI Trending Topics`, and `Content Hub`. |
| ✉️ **Daily Digest** | Emails you an HTML summary of top tweets, topics, and content opportunities for the day. |

---

## 🧱 Workflow Architecture
X Scraper → Topic Analysis → Perplexity Research →
AI Content Brainstorm → Report Generation →
Email Digest + Notion Upload

Each step uses structured prompts, GPT-based parsing, and JSON schema validation to maintain accuracy and consistency.

---

## 🔧 Setup Instructions

### 1️⃣ Requirements
You’ll need accounts for:
- [Apify](https://www.apify.com?fpr=92rji7) (for X/Twitter scraping)
- [Perplexity API](https://www.perplexity.ai/)
- [OpenRouter](https://openrouter.ai/)
- [Notion](https://www.notion.so/)

### 2️⃣ Import the Workflow
1. Download the Social Media Story Scraper.json file.  
2. In n8n, click **Import Workflow** → upload the JSON.  
3. Set your **credentials** for Apify, Perplexity, OpenRouter, Gmail, and Notion.  
4. Edit the “Set X List URL” node to target your desired X List or search term.  
   Example:
   ```js
   "https://x.com/i/lists/1944053485882028279"

## 🧠 Example Use Cases

- Content Creators: Identify trending narratives early and generating video ideas.
- Marketing Teams: Monitoring AI, tech, and industry chatter for campaign ideas.
- Media Companies: Automating editorial research workflows.
- AI Enthusiasts: Build data-driven content around emerging tech conversations.



