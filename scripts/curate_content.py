#!/usr/bin/env python3
"""
Content Curator - International Politics & Swedish News
Uses Claude to filter, categorize, and summarize news for the weekly digest
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import anthropic
import os

class ContentCurator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def get_latest_raw_data(self) -> Dict[str, Any]:
        """Load the most recent raw news data"""
        data_files = sorted(self.data_dir.glob("raw_news_*.json"), reverse=True)

        if not data_files:
            raise FileNotFoundError("No raw news data found. Run collect_news.py first.")

        with open(data_files[0], encoding='utf-8') as f:
            return json.load(f)

    async def categorize_and_summarize(self, news_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use Claude to intelligently categorize and summarize the news"""
        print("🧠 Using Claude to curate content...\n")

        articles = news_data['articles']

        # Prepare articles for Claude
        articles_summary = []
        for idx, article in enumerate(articles[:100], 1):  # Limit to 100 for token efficiency
            articles_summary.append({
                'id': idx,
                'source': article['source'],
                'title': article['title'],
                'summary': article['summary'][:300],
                'url': article['url']
            })

        # Create prompt for Claude
        prompt = f"""Curate weekly digest for international politics, war updates, Swedish news.

{len(articles_summary)} articles from this week. Tasks:

1. Filter most relevant/important articles
2. Categorize into sections:
   - International Politics (diplomatic developments, elections, policy changes)
   - War & Conflict (military operations, conflicts, peace negotiations)
   - Swedish News (Swedish politics, economy, society)
   - Diplomacy & Relations (international relations, treaties, summits)

3. For each selected article provide:
   - Section assignment
   - One-sentence insight explaining significance
   - Relevance score (1-10)

4. Select TOP 8-10 items per section (most significant stories)

Articles:

{json.dumps(articles_summary, indent=2, ensure_ascii=False)}

CRITICAL: Return ONLY valid JSON. No markdown, no code blocks, no explanatory text. Start with {{ and end with }}.

Structure:
{{
  "sections": {{
    "International Politics": [
      {{"id": 1, "title": "...", "url": "...", "source": "...", "insight": "...", "score": 9}}
    ],
    "War & Conflict": [],
    "Swedish News": [],
    "Diplomacy & Relations": []
  }},
  "weekly_summary": "2-3 sentence summary of week's major themes"
}}"""

        # Call Claude with higher token limit for complete JSON
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Parse JSON response
        try:
            # Remove markdown code blocks if present
            json_str = response_text.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:]
            elif json_str.startswith('```'):
                json_str = json_str[3:]
            if json_str.endswith('```'):
                json_str = json_str[:-3]

            json_str = json_str.strip()

            # Find JSON bounds
            json_start = json_str.find('{')
            json_end = json_str.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No valid JSON object found in response")

            json_str = json_str[json_start:json_end]

            curated = json.loads(json_str)

            # Enrich with full article data
            article_map = {idx: article for idx, article in enumerate(articles[:100], 1)}

            for section_name, items in curated['sections'].items():
                for item in items:
                    article_id = item.get('id')
                    if article_id and article_id in article_map:
                        original = article_map[article_id]
                        item['summary'] = original.get('summary', '')
                        item['published'] = original.get('published', '')
                        if not item.get('source'):
                            item['source'] = original.get('source', 'Unknown')

        except json.JSONDecodeError as e:
            print(f"Error parsing Claude response: {e}")
            print(f"Response: {response_text}")
            raise

        # Save curated content
        output_file = self.data_dir / f"curated_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(curated, f, indent=2, ensure_ascii=False)

        # Print summary
        print("✅ Content curated successfully!\n")
        print(f"Weekly theme: {curated['weekly_summary']}\n")

        for section_name, items in curated['sections'].items():
            print(f"  {section_name}: {len(items)} items")

        print(f"\n📁 Saved to: {output_file}")

        return curated

    async def curate(self) -> Dict[str, Any]:
        """Main curation workflow"""
        print("🎯 Starting content curation...\n")

        # Load raw data
        raw_data = self.get_latest_raw_data()
        print(f"📊 Loaded raw data with {len(raw_data['articles'])} articles\n")

        # Curate with Claude
        curated = await self.categorize_and_summarize(raw_data)

        return curated

async def main():
    curator = ContentCurator()
    await curator.curate()

if __name__ == "__main__":
    asyncio.run(main())
