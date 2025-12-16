#!/usr/bin/env python3
"""
News Aggregator - International Politics & Swedish News
Collects news from RSS feeds for weekly digest
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
import feedparser
import requests
from typing import List, Dict, Any

class NewsCollector:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)

        self.today = datetime.now()
        self.week_ago = self.today - timedelta(days=7)

        # RSS feed sources
        self.feeds = {
            'guardian': 'https://www.theguardian.com/world/rss',
            'bbc_world': 'https://feeds.bbci.co.uk/news/world/rss.xml',
            'aljazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
            'reuters': 'https://www.reuters.com/rssfeed/worldNews',
            'svenska_dagbladet': 'https://www.svd.se/?service=rss',
            'dagens_nyheter': 'https://www.dn.se/rss/',
            'aftonbladet': 'https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/',
            'thelocal_sweden': 'https://feeds.thelocal.com/rss/se'
        }

    async def collect_from_feed(self, source_name: str, feed_url: str) -> List[Dict[str, Any]]:
        """Collect articles from a single RSS feed"""
        print(f"  Collecting from {source_name}...")
        articles = []

        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:50]:  # Check up to 50 recent items
                try:
                    # Parse publication date
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        published = datetime(*entry.updated_parsed[:6])
                    else:
                        published = self.today

                    # Only include articles from the past week
                    if published >= self.week_ago:
                        article = {
                            'source': source_name,
                            'title': entry.get('title', ''),
                            'summary': entry.get('summary', entry.get('description', ''))[:500],
                            'url': entry.get('link', ''),
                            'published': published.isoformat(),
                            'author': entry.get('author', 'Unknown')
                        }
                        articles.append(article)
                except Exception as e:
                    print(f"    Warning: Skipped entry - {e}")
                    continue

            print(f"    Found {len(articles)} recent articles")
        except Exception as e:
            print(f"    Error collecting from {source_name}: {e}")

        return articles

    async def collect_all(self) -> Dict[str, Any]:
        """Collect from all RSS feeds"""
        print("\n📰 Starting news collection...\n")

        all_articles = []

        # Collect from each feed sequentially (to avoid rate limiting)
        for source_name, feed_url in self.feeds.items():
            articles = await self.collect_from_feed(source_name, feed_url)
            all_articles.extend(articles)
            await asyncio.sleep(1)  # Be respectful to servers

        news_data = {
            'articles': all_articles,
            'collected_at': self.today.isoformat(),
            'week_start': self.week_ago.isoformat(),
            'week_end': self.today.isoformat(),
            'total_articles': len(all_articles)
        }

        # Save raw data
        output_file = self.data_dir / f"raw_news_{self.today.strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Collection complete! Found {len(all_articles)} articles")
        print(f"📁 Saved to: {output_file}")

        return news_data

async def main():
    collector = NewsCollector()
    await collector.collect_all()

if __name__ == "__main__":
    asyncio.run(main())
