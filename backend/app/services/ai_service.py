"""AI Analysis Service - Multi-provider support for Claude, Gemini, and GPT"""
import json
from typing import Dict, Any, List, Optional
import openai
from anthropic import Anthropic
import google.generativeai as genai
from ..models.user_preferences import AIProvider


class AIAnalysisService:
    """Unified AI service supporting multiple providers"""

    def __init__(self, provider: AIProvider, model_name: str, api_key: str):
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate AI client"""
        if self.provider == AIProvider.OPENAI:
            openai.api_key = self.api_key
            self.client = openai
        elif self.provider == AIProvider.ANTHROPIC:
            self.client = Anthropic(api_key=self.api_key)
        elif self.provider == AIProvider.GOOGLE:
            genai.configure(api_key=self.api_key)
            self.client = genai

    async def analyze_tweets(self, tweets_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze tweets to identify top tweets and trending topics

        Returns:
        {
            "top_tweets": [...],
            "trending_topics": [...]
        }
        """
        prompt = self._build_tweet_analysis_prompt(tweets_data)

        if self.provider == AIProvider.OPENAI:
            return await self._analyze_with_openai(prompt)
        elif self.provider == AIProvider.ANTHROPIC:
            return await self._analyze_with_claude(prompt)
        elif self.provider == AIProvider.GOOGLE:
            return await self._analyze_with_gemini(prompt)

    async def generate_content_ideas(
        self,
        twitter_data: Dict[str, Any],
        perplexity_data: str
    ) -> Dict[str, Any]:
        """
        Generate content ideas based on trending topics

        Returns:
        {
            "content_ideas": [...]
        }
        """
        prompt = self._build_content_generation_prompt(twitter_data, perplexity_data)

        if self.provider == AIProvider.OPENAI:
            return await self._generate_with_openai(prompt)
        elif self.provider == AIProvider.ANTHROPIC:
            return await self._generate_with_claude(prompt)
        elif self.provider == AIProvider.GOOGLE:
            return await self._generate_with_gemini(prompt)

    def _build_tweet_analysis_prompt(self, tweets_data: List[Dict[str, Any]]) -> str:
        """Build prompt for tweet analysis"""
        return f"""You are an AI Social Media Analyst. Analyze the following tweets and identify:
1. Top 5 tweets by engagement score (calculate as: likes + 2×retweets + 0.5×replies / follower_count)
2. Top 5 trending topics across all tweets

Tweets data:
{json.dumps(tweets_data, indent=2)}

Return a JSON response with this structure:
{{
  "top_tweets": [
    {{
      "rank": 1,
      "tweet_id": "...",
      "text": "...",
      "like_count": 0,
      "engagement_score": 0.0,
      "url": "..."
    }}
  ],
  "trending_topics": [
    {{
      "rank": 1,
      "title": "Topic Title",
      "description": "3-4 sentence description of the topic and why it's trending"
    }}
  ]
}}"""

    def _build_content_generation_prompt(
        self,
        twitter_data: Dict[str, Any],
        perplexity_data: str
    ) -> str:
        """Build prompt for content idea generation"""
        return f"""You are an elite content strategist. Based on the trending topics and research below, generate 3-5 strategic content ideas.

Twitter Trending Topics:
{json.dumps(twitter_data.get('trending_topics', []), indent=2)}

Perplexity Research:
{perplexity_data}

Generate content ideas following viral content principles (curiosity gaps, contrast, viewer-centric framing).

Return a JSON response with this structure:
{{
  "content_ideas": [
    {{
      "title": "Compelling title with curiosity gap",
      "content_overview": "2-3 paragraphs explaining the content",
      "target_audience": "Specific audience description",
      "core_pain_point": "Main problem being solved",
      "hook_strategy": {{
        "key_visual": "Description of opening visual",
        "text_hook": "3-5 bold words",
        "spoken_hook": "Opening line that creates contrast"
      }},
      "storyline_outline": {{
        "intro": "Hook confirmation and plan",
        "main_points": ["Point 1", "Point 2", "Point 3"],
        "outro": "Summary and CTA"
      }}
    }}
  ]
}}"""

    async def _analyze_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Analyze using OpenAI GPT"""
        try:
            response = await self.client.ChatCompletion.acreate(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI analyst. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"OpenAI analysis error: {str(e)}")

    async def _analyze_with_claude(self, prompt: str) -> Dict[str, Any]:
        """Analyze using Anthropic Claude"""
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.content[0].text
            return json.loads(content)
        except Exception as e:
            raise Exception(f"Claude analysis error: {str(e)}")

    async def _analyze_with_gemini(self, prompt: str) -> Dict[str, Any]:
        """Analyze using Google Gemini"""
        try:
            model = self.client.GenerativeModel(self.model_name)
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            raise Exception(f"Gemini analysis error: {str(e)}")

    async def _generate_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Generate content ideas using OpenAI"""
        return await self._analyze_with_openai(prompt)

    async def _generate_with_claude(self, prompt: str) -> Dict[str, Any]:
        """Generate content ideas using Claude"""
        return await self._analyze_with_claude(prompt)

    async def _generate_with_gemini(self, prompt: str) -> Dict[str, Any]:
        """Generate content ideas using Gemini"""
        return await self._analyze_with_gemini(prompt)
