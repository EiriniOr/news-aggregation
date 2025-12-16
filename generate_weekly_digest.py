#!/usr/bin/env python3
"""
Global News Weekly Digest Generator
Main orchestrator script that collects, curates, and generates the presentation
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from collect_news import NewsCollector
from curate_content import ContentCurator
from generate_webpage import WebpageGenerator
from deploy_github import deploy_to_github
from generate_audio import AudioGenerator

async def generate_weekly_digest():
    """Run the complete weekly digest pipeline"""
    print("=" * 70)
    print("  🌍 GLOBAL NEWS WEEKLY DIGEST GENERATOR")
    print("=" * 70)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    try:
        # Step 1: Collect news
        print("STEP 1/5: Collecting news from international sources")
        print("-" * 70)
        collector = NewsCollector()
        news_data = await collector.collect_all()
        print()

        # Step 2: Curate content
        print("STEP 2/5: Curating and filtering content with Claude")
        print("-" * 70)
        curator = ContentCurator()
        curated_data = await curator.curate()
        print()

        # Step 3: Generate webpage
        print("STEP 3/5: Generating professional webpage")
        print("-" * 70)
        generator = WebpageGenerator()
        filepath = await generator.generate()
        print()

        # Step 4: Generate audio narration
        print("STEP 4/5: Generating audio narration")
        print("-" * 70)
        audio_gen = AudioGenerator()
        audio_path = await audio_gen.generate()
        print()

        # Step 5: Deploy to GitHub Pages
        print("STEP 5/5: Preparing GitHub Pages deployment")
        print("-" * 70)
        github_deployed = await deploy_to_github(filepath)
        print()

        # Success summary
        print("=" * 70)
        print("  ✅ SUCCESS!")
        print("=" * 70)
        print(f"\n  Your weekly news digest webpage is ready:")
        print(f"  📄 {filepath}")
        if github_deployed:
            print(f"  🚀 Ready to deploy to GitHub Pages")
        if audio_path:
            print(f"  🎙️  Audio narration: {audio_path}")
        print(f"\n  Open the webpage in your browser to view the digest!")
        print()

        return filepath

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure to run the steps in order.")
        return None

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    filepath = await generate_weekly_digest()

    if filepath:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
