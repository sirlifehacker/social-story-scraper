"""Perplexity AI Research Service"""
import httpx
from typing import List, Dict, Any


class PerplexityService:
    """Service for deep research using Perplexity AI"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"

    async def research_topics(self, topics: List[Dict[str, Any]]) -> str:
        """
        Research trending topics using Perplexity AI

        Args:
            topics: List of trending topic dictionaries with 'title' and 'description'

        Returns:
            Research insights as formatted text
        """
        # Build research prompt
        topics_text = "\n\n".join([
            f"{i+1}: {topic['title']}\n{topic['description']}"
            for i, topic in enumerate(topics[:5])  # Top 5 topics
        ])

        prompt = f"""You are a research assistant. For each of the following trending topics, find and summarize the most recent & credible information available online. Focus on finding insights that are unique, lesser known, and novel.

Topics:
{topics_text}

For each topic, output:
- A 7-10 sentence overview of the insights found
- A visual analogy of the key insight from the topic
- What niches stand to benefit most from the topic and how."""

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "sonar-pro",
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPError as e:
            raise Exception(f"Perplexity research error: {str(e)}")

    def parse_research_results(self, research_text: str) -> List[Dict[str, Any]]:
        """
        Parse Perplexity research results into structured data

        Returns:
            List of research insights for each topic
        """
        # This is a simple parser - in production, you might use AI to structure this
        results = []

        # Split by topic numbers (1:, 2:, etc.)
        sections = research_text.split("\n\n")

        current_topic = {}
        for section in sections:
            if section.strip():
                # Simple parsing - can be enhanced with regex or AI
                if any(section.startswith(f"{i}:") for i in range(1, 6)):
                    if current_topic:
                        results.append(current_topic)
                    current_topic = {"raw_text": section}
                else:
                    if current_topic:
                        current_topic["raw_text"] = current_topic.get("raw_text", "") + "\n\n" + section

        if current_topic:
            results.append(current_topic)

        return results
