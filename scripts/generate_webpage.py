#!/usr/bin/env python3
"""
Webpage Generator - International Politics & Swedish News
Creates a professional news website with multi-column layout
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

class WebpageGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

    def get_latest_curated_data(self):
        """Load the most recent curated content"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)

        if not data_files:
            raise FileNotFoundError("No curated data found. Run curate_content.py first.")

        with open(data_files[0], encoding='utf-8') as f:
            return json.load(f)

    def get_recent_digests(self, limit=5):
        """Get list of recent digest files"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)
        return data_files[:limit]

    async def create_webpage(self, curated_data):
        """Generate professional news webpage with multi-column layout"""
        print("🎨 Creating webpage...\n")

        date_str = datetime.now().strftime('%Y%m%d')
        week_str = datetime.now().strftime('%B %d, %Y')

        # Get recent digests for archive
        recent_digests = self.get_recent_digests(5)
        archive_html = ""

        for idx, digest_file in enumerate(recent_digests):
            with open(digest_file, encoding='utf-8') as f:
                digest_data = json.load(f)

            digest_date = digest_file.stem.replace('curated_', '')
            formatted_date = datetime.strptime(digest_date, '%Y%m%d').strftime('%B %d, %Y')

            total_items = sum(len(items) for items in digest_data.get('sections', {}).values())

            # Create individual archive page for older digests
            if idx > 0:
                archive_filename = f"digest-{digest_date}.html"
                await self.create_archive_page(digest_data, digest_date, archive_filename)

                archive_html += f"""
                <a href="{archive_filename}" class="archive-link">
                    <div class="archive-item">
                        <div class="archive-date">{formatted_date}</div>
                        <div class="archive-summary">{digest_data.get('weekly_summary', '')[:120]}...</div>
                        <div class="archive-stats">{total_items} articles</div>
                    </div>
                </a>
                """
            else:
                # Current week
                archive_html += f"""
                <div class="archive-item current-week">
                    <div class="archive-date">{formatted_date} (Current)</div>
                    <div class="archive-summary">{digest_data.get('weekly_summary', '')[:120]}...</div>
                    <div class="archive-stats">{total_items} articles</div>
                </div>
                """

        # Build sections HTML with multi-column layout
        sections_html = ""
        sections = curated_data.get('sections', {})

        section_icons = {
            "International Politics": "🌍",
            "War & Conflict": "⚔️",
            "Swedish News": "🇸🇪",
            "Diplomacy & Relations": "🤝"
        }

        section_colors = {
            "International Politics": "#1e3a8a",
            "War & Conflict": "#991b1b",
            "Swedish News": "#065f46",
            "Diplomacy & Relations": "#7c2d12"
        }

        for section_name, items in sections.items():
            if not items:
                continue

            icon = section_icons.get(section_name, "📰")
            color = section_colors.get(section_name, "#1e40af")

            items_html = ""
            for item in items:
                title = item.get('title', '')
                insight = item.get('insight', '')
                source = item.get('source', 'Unknown').replace('_', ' ').title()
                url = item.get('url', '')

                url_html = f'<a href="{url}" target="_blank" class="item-link">Read article →</a>' if url else ''

                items_html += f"""
                <div class="content-item">
                    <h3 class="item-title">{title}</h3>
                    <p class="item-insight">{insight}</p>
                    <div class="item-meta">
                        <span class="meta-source">{source}</span>
                        {url_html}
                    </div>
                </div>
                """

            sections_html += f"""
            <section class="content-section" style="border-left: 4px solid {color}">
                <h2 class="section-title">{icon} {section_name}</h2>
                <div class="section-items">
                    {items_html}
                </div>
            </section>
            """

        # Create HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global News Weekly - International Politics & Swedish News</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #f5f5f5;
            color: #1a1a1a;
            line-height: 1.7;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0;
        }}

        /* Header */
        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 60px 40px 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }}

        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .header h1 {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: -1px;
        }}

        .header .subtitle {{
            font-size: 1.3rem;
            opacity: 0.95;
            font-weight: 300;
            margin-bottom: 15px;
        }}

        .header .date {{
            font-size: 1.1rem;
            opacity: 0.85;
            font-weight: 300;
        }}

        /* Audio Section */
        .audio-container {{
            background: #1e40af;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .audio-content {{
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }}

        .audio-content h2 {{
            color: white;
            font-size: 1.5rem;
            margin-bottom: 20px;
            font-weight: 400;
        }}

        .audio-content audio {{
            width: 100%;
            max-width: 700px;
            margin: 0 auto;
            display: block;
        }}

        .audio-content p {{
            color: rgba(255,255,255,0.8);
            margin-top: 15px;
            font-size: 0.95rem;
        }}

        /* Main Content */
        .main-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        /* Summary */
        .summary {{
            background: white;
            border-left: 5px solid #1e40af;
            padding: 35px;
            margin-bottom: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .summary h2 {{
            color: #1e40af;
            margin-bottom: 18px;
            font-size: 1.8rem;
            font-weight: 600;
        }}

        .summary p {{
            font-size: 1.15rem;
            line-height: 1.8;
            color: #374151;
        }}

        /* Content Sections */
        .content-section {{
            background: white;
            padding: 35px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .section-title {{
            font-size: 2rem;
            margin-bottom: 30px;
            color: #1a1a1a;
            font-weight: 600;
            padding-bottom: 15px;
            border-bottom: 2px solid #e5e7eb;
        }}

        .section-items {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }}

        .content-item {{
            background: #fafafa;
            padding: 25px;
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
        }}

        .content-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            background: white;
        }}

        .item-title {{
            color: #1a1a1a;
            margin-bottom: 12px;
            font-size: 1.25rem;
            font-weight: 600;
            line-height: 1.4;
        }}

        .item-insight {{
            color: #4b5563;
            margin-bottom: 18px;
            font-size: 1rem;
            line-height: 1.6;
        }}

        .item-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            padding-top: 15px;
            border-top: 1px solid #e5e7eb;
            font-size: 0.9rem;
        }}

        .meta-source {{
            color: #6b7280;
            font-weight: 500;
        }}

        .item-link {{
            color: #1e40af;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}

        .item-link:hover {{
            color: #3b82f6;
            text-decoration: underline;
        }}

        /* Archive Section */
        .archive {{
            background: white;
            padding: 35px;
            margin-top: 40px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .archive h2 {{
            color: #1e40af;
            margin-bottom: 25px;
            font-size: 1.8rem;
            font-weight: 600;
        }}

        .archive-link {{
            text-decoration: none;
            display: block;
            transition: transform 0.2s;
        }}

        .archive-link:hover {{
            transform: translateX(5px);
        }}

        .archive-item {{
            background: #fafafa;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #1e40af;
            transition: all 0.2s;
        }}

        .archive-link .archive-item:hover {{
            background: #f3f4f6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .archive-item.current-week {{
            border-left: 4px solid #3b82f6;
        }}

        .archive-date {{
            color: #1e40af;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 1.05rem;
        }}

        .archive-summary {{
            color: #4b5563;
            font-size: 0.95rem;
            margin-bottom: 8px;
            line-height: 1.5;
        }}

        .archive-stats {{
            color: #6b7280;
            font-size: 0.85rem;
        }}

        /* Footer */
        .footer {{
            background: #1f2937;
            color: #d1d5db;
            text-align: center;
            padding: 40px 20px;
            margin-top: 60px;
        }}

        .footer p {{
            margin-bottom: 10px;
        }}

        .footer a {{
            color: #93c5fd;
            text-decoration: none;
        }}

        .footer a:hover {{
            color: #bfdbfe;
            text-decoration: underline;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2.5rem;
            }}

            .section-items {{
                grid-template-columns: 1fr;
            }}

            .content-item {{
                padding: 20px;
            }}

            .item-meta {{
                flex-direction: column;
                align-items: flex-start;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <div class="header">
        <div class="header-content">
            <h1>Global News Weekly</h1>
            <p class="subtitle">International Politics, Conflict Analysis & Diplomatic Relations</p>
            <p class="date">Week of {week_str}</p>
        </div>
    </div>

    <!-- Audio Narration -->
    <div class="audio-container">
        <div class="audio-content">
            <h2>Listen to This Week's Digest</h2>
            <audio controls>
                <source src="audio/narration_{date_str}.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <p>AI-narrated summary of this week's most important global news</p>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <!-- Summary -->
        <div class="summary">
            <h2>This Week's Overview</h2>
            <p>{curated_data.get('weekly_summary', 'Your weekly international news digest')}</p>
        </div>

        <!-- Content Sections -->
        {sections_html}

        <!-- Archive -->
        <div class="archive">
            <h2>Recent Editions</h2>
            {archive_html}
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        <p>Sources: The Guardian, BBC, Al Jazeera, Reuters, New York Times, AP News, NPR, Financial Times</p>
        <p>Automatically generated every Monday at 6:00 AM UTC</p>
        <p style="margin-top: 20px; opacity: 0.7; font-size: 14px;">
            Created by Eirini Ornithopoulou, for Meli, 2025
        </p>
    </div>
</body>
</html>
"""

        # Write HTML file
        output_path = self.output_dir / "index.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Webpage created successfully!")
        print(f"📁 Location: {output_path}")

        return output_path

    async def create_archive_page(self, curated_data, date_str, filename):
        """Create an individual archive page for a past digest"""
        formatted_date = datetime.strptime(date_str, '%Y%m%d').strftime('%B %d, %Y')

        # Build sections HTML
        sections_html = ""
        sections = curated_data.get('sections', {})

        section_icons = {
            "International Politics": "🌍",
            "War & Conflict": "⚔️",
            "Swedish News": "🇸🇪",
            "Diplomacy & Relations": "🤝"
        }

        section_colors = {
            "International Politics": "#1e3a8a",
            "War & Conflict": "#991b1b",
            "Swedish News": "#065f46",
            "Diplomacy & Relations": "#7c2d12"
        }

        for section_name, items in sections.items():
            if not items:
                continue

            icon = section_icons.get(section_name, "📰")
            color = section_colors.get(section_name, "#1e40af")

            items_html = ""
            for item in items:
                title = item.get('title', '')
                insight = item.get('insight', '')
                source = item.get('source', 'Unknown').replace('_', ' ').title()
                url = item.get('url', '')

                url_html = f'<a href="{url}" target="_blank" class="item-link">Read article →</a>' if url else ''

                items_html += f"""
                <div class="content-item">
                    <h3 class="item-title">{title}</h3>
                    <p class="item-insight">{insight}</p>
                    <div class="item-meta">
                        <span class="meta-source">{source}</span>
                        {url_html}
                    </div>
                </div>
                """

            sections_html += f"""
            <section class="content-section" style="border-left: 4px solid {color}">
                <h2 class="section-title">{icon} {section_name}</h2>
                <div class="section-items">
                    {items_html}
                </div>
            </section>
            """

        # Use same CSS as main page (abbreviated for brevity)
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global News Weekly - {formatted_date}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', 'Times New Roman', serif; background: #f5f5f5; color: #1a1a1a; line-height: 1.7; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 0; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 60px 40px 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); }}
        .header-content {{ max-width: 1200px; margin: 0 auto; }}
        .header h1 {{ font-size: 3.5rem; font-weight: 700; margin-bottom: 15px; letter-spacing: -1px; }}
        .header .subtitle {{ font-size: 1.3rem; opacity: 0.95; font-weight: 300; margin-bottom: 15px; }}
        .header .date {{ font-size: 1.1rem; opacity: 0.85; font-weight: 300; }}
        .back-link {{ display: inline-block; margin: 20px 40px; color: #1e40af; text-decoration: none; font-size: 1.1rem; font-weight: 500; }}
        .back-link:hover {{ color: #3b82f6; text-decoration: underline; }}
        .main-content {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}
        .summary {{ background: white; border-left: 5px solid #1e40af; padding: 35px; margin-bottom: 40px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .summary h2 {{ color: #1e40af; margin-bottom: 18px; font-size: 1.8rem; font-weight: 600; }}
        .summary p {{ font-size: 1.15rem; line-height: 1.8; color: #374151; }}
        .content-section {{ background: white; padding: 35px; margin-bottom: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .section-title {{ font-size: 2rem; margin-bottom: 30px; color: #1a1a1a; font-weight: 600; padding-bottom: 15px; border-bottom: 2px solid #e5e7eb; }}
        .section-items {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px; }}
        .content-item {{ background: #fafafa; padding: 25px; border: 1px solid #e5e7eb; transition: all 0.3s ease; }}
        .content-item:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); background: white; }}
        .item-title {{ color: #1a1a1a; margin-bottom: 12px; font-size: 1.25rem; font-weight: 600; line-height: 1.4; }}
        .item-insight {{ color: #4b5563; margin-bottom: 18px; font-size: 1rem; line-height: 1.6; }}
        .item-meta {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; padding-top: 15px; border-top: 1px solid #e5e7eb; font-size: 0.9rem; }}
        .meta-source {{ color: #6b7280; font-weight: 500; }}
        .item-link {{ color: #1e40af; text-decoration: none; font-weight: 500; transition: color 0.2s; }}
        .item-link:hover {{ color: #3b82f6; text-decoration: underline; }}
        .footer {{ background: #1f2937; color: #d1d5db; text-align: center; padding: 40px 20px; margin-top: 60px; }}
        .footer a {{ color: #93c5fd; text-decoration: none; }}
        .footer a:hover {{ color: #bfdbfe; text-decoration: underline; }}
        @media (max-width: 768px) {{ .header h1 {{ font-size: 2.5rem; }} .section-items {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <a href="index.html" class="back-link">← Back to Latest Digest</a>

    <div class="header">
        <div class="header-content">
            <h1>Global News Weekly</h1>
            <p class="subtitle">Archived Edition</p>
            <p class="date">{formatted_date}</p>
        </div>
    </div>

    <div class="main-content">
        <div class="summary">
            <h2>This Week's Overview</h2>
            <p>{curated_data.get('weekly_summary', 'Your weekly international news digest')}</p>
        </div>

        {sections_html}
    </div>

    <div class="footer">
        <p>Sources: The Guardian, BBC, Al Jazeera, Reuters, New York Times, AP News, NPR, Financial Times</p>
        <p style="margin-top: 20px; font-size: 0.9em;">Created by Eirini Ornithopoulou, for Meli, 2025</p>
    </div>
</body>
</html>
"""

        # Write archive HTML file
        archive_path = self.output_dir / filename
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"  ✓ Created archive page: {filename}")

    async def generate(self):
        """Main generation workflow"""
        print("🎯 Starting webpage generation...\n")

        # Load curated data
        curated_data = self.get_latest_curated_data()

        total_items = sum(len(items) for items in curated_data.get('sections', {}).values())
        print(f"📊 Loaded curated content with {total_items} items\n")

        # Create webpage
        filepath = await self.create_webpage(curated_data)

        return filepath

async def main():
    generator = WebpageGenerator()
    filepath = await generator.generate()
    print(f"\n🎉 Done! Open your webpage:\n   {filepath}")

if __name__ == "__main__":
    asyncio.run(main())
