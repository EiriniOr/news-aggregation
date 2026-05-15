#!/usr/bin/env python3
"""
Webpage Generator - International Politics
Creates a futuristic 'newsroom aurora' webpage
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path


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
            raise FileNotFoundError(
                "No curated data found. Run curate_content.py first."
            )
        with open(data_files[0], encoding="utf-8") as f:
            return json.load(f)

    async def create_webpage(self, curated_data):
        """Generate aurora-themed news webpage"""
        print("🎨 Creating webpage...\n")

        date_str = datetime.now().strftime("%Y%m%d")
        week_str = datetime.now().strftime("%B %d, %Y")

        sections_html = ""
        sections = curated_data.get("sections", {})

        section_meta = {
            "International Politics": {
                "icon": "🌍",
                "color": "#fbbf24",
                "glow": "rgba(251, 191, 36, 0.45)",
            },
            "War & Conflict": {
                "icon": "⚔️",
                "color": "#ef4444",
                "glow": "rgba(239, 68, 68, 0.45)",
            },
            "Diplomacy & Relations": {
                "icon": "🤝",
                "color": "#14b8a6",
                "glow": "rgba(20, 184, 166, 0.45)",
            },
        }

        for section_name, items in sections.items():
            if not items:
                continue

            meta = section_meta.get(
                section_name,
                {"icon": "📰", "color": "#3b82f6", "glow": "rgba(59, 130, 246, 0.45)"},
            )
            icon = meta["icon"]
            color = meta["color"]
            glow = meta["glow"]

            items_html = ""
            for item in items:
                title = item.get("title", "")
                insight = item.get("insight", "")
                source = item.get("source", "Unknown").replace("_", " ").title()
                url = item.get("url", "")
                url_html = (
                    f'<a href="{url}" target="_blank" class="item-link">read article →</a>'
                    if url
                    else ""
                )

                items_html += f"""
                <article class="content-item">
                    <h3 class="item-title">{title}</h3>
                    <p class="item-insight">{insight}</p>
                    <div class="item-meta">
                        <span class="meta-source">{source}</span>
                        {url_html}
                    </div>
                </article>
                """

            sections_html += f"""
            <section class="content-section" style="--accent: {color}; --accent-glow: {glow};">
                <h2 class="section-title"><span class="section-icon">{icon}</span>{section_name}</h2>
                <div class="section-items">
                    {items_html}
                </div>
            </section>
            """

        weekly_summary = curated_data.get(
            "weekly_summary", "Your weekly international news digest"
        )

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global News Weekly — International Politics</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-0: #060912;
            --bg-1: #0a0e1a;
            --bg-2: #111827;
            --amber: #fbbf24;
            --amber-soft: #f59e0b;
            --crimson: #ef4444;
            --teal: #14b8a6;
            --blue: #3b82f6;
            --text: #e5e7eb;
            --text-dim: #9ca3af;
            --text-muted: #6b7280;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-0);
            color: var(--text);
            line-height: 1.65;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }}

        /* Layered aurora background */
        body::before {{
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 70% 50% at 10% 5%, rgba(251, 191, 36, 0.12), transparent 60%),
                radial-gradient(ellipse 60% 45% at 90% 15%, rgba(239, 68, 68, 0.10), transparent 60%),
                radial-gradient(ellipse 80% 60% at 50% 95%, rgba(20, 184, 166, 0.12), transparent 65%),
                radial-gradient(ellipse 50% 50% at 85% 80%, rgba(59, 130, 246, 0.08), transparent 60%),
                linear-gradient(180deg, #060912 0%, #0a0e1a 55%, #111827 100%);
            z-index: -3;
            animation: auroraShift 40s ease-in-out infinite alternate;
        }}

        @keyframes auroraShift {{
            0%   {{ filter: hue-rotate(0deg) brightness(1); }}
            100% {{ filter: hue-rotate(-15deg) brightness(1.08); }}
        }}

        /* Animated horizontal scanlines (newsroom-monitor feel) */
        .grid-overlay {{
            position: fixed;
            inset: 0;
            z-index: -2;
            pointer-events: none;
            background-image:
                linear-gradient(180deg, transparent 0%, rgba(251, 191, 36, 0.03) 50%, transparent 100%);
            background-size: 100% 6px;
            animation: scanMove 8s linear infinite;
            opacity: 0.6;
        }}

        @keyframes scanMove {{
            from {{ background-position: 0 0; }}
            to   {{ background-position: 0 24px; }}
        }}

        /* Subtle pinpoint lights — distant city/news beacons */
        .lights {{
            position: fixed;
            inset: 0;
            z-index: -2;
            pointer-events: none;
            overflow: hidden;
        }}

        .lights::before {{
            content: '';
            position: absolute;
            inset: -30%;
            background-image:
                radial-gradient(1.5px 1.5px at 50px 80px, var(--amber), transparent),
                radial-gradient(1px 1px at 130px 40px, var(--text), transparent),
                radial-gradient(1.5px 1.5px at 220px 110px, var(--teal), transparent),
                radial-gradient(1px 1px at 290px 60px, var(--text), transparent),
                radial-gradient(2px 2px at 360px 30px, var(--crimson), transparent),
                radial-gradient(1px 1px at 410px 130px, var(--text), transparent);
            background-size: 500px 200px;
            background-repeat: repeat;
            opacity: 0.4;
            animation: lightDrift 180s linear infinite;
        }}

        @keyframes lightDrift {{
            from {{ transform: translate(0, 0); }}
            to   {{ transform: translate(-500px, -200px); }}
        }}

        /* Cursor spotlight */
        .cursor-glow {{
            position: fixed;
            width: 480px;
            height: 480px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(251, 191, 36, 0.10), transparent 70%);
            pointer-events: none;
            z-index: -1;
            transform: translate(-50%, -50%);
            mix-blend-mode: screen;
        }}

        .container {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 22px 24px 60px;
            position: relative;
        }}

        /* Compact masthead */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            padding: 16px 24px;
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.08), rgba(20, 184, 166, 0.06));
            border: 1px solid rgba(251, 191, 36, 0.25);
            border-radius: 14px;
            margin-bottom: 28px;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            box-shadow: 0 4px 26px rgba(251, 191, 36, 0.12);
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 2px;
            background: linear-gradient(90deg, transparent, var(--amber), var(--crimson), transparent);
            animation: tickerSweep 5s ease-in-out infinite;
        }}

        @keyframes tickerSweep {{
            0%, 100% {{ left: -100%; }}
            50%      {{ left: 100%; }}
        }}

        .brand {{ display: flex; align-items: center; gap: 14px; }}

        .brand-mark {{
            width: 42px; height: 42px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--amber), var(--crimson));
            display: flex; align-items: center; justify-content: center;
            font-size: 22px;
            box-shadow: 0 0 18px rgba(251, 191, 36, 0.45);
        }}

        .header h1 {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #fff 0%, var(--amber) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.01em;
            line-height: 1.1;
        }}

        .header .tagline {{
            font-size: 0.76rem;
            color: var(--text-muted);
            font-family: 'JetBrains Mono', monospace;
            margin-top: 3px;
        }}

        .date-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: var(--amber);
            padding: 6px 14px;
            border: 1px solid rgba(251, 191, 36, 0.35);
            border-radius: 999px;
            background: rgba(251, 191, 36, 0.06);
            white-space: nowrap;
        }}

        /* Podcast hero */
        .podcast-hero {{
            position: relative;
            padding: 34px 32px;
            margin-bottom: 32px;
            border-radius: 22px;
            background:
                radial-gradient(ellipse at top left, rgba(251, 191, 36, 0.20), transparent 60%),
                radial-gradient(ellipse at bottom right, rgba(239, 68, 68, 0.18), transparent 60%),
                rgba(10, 14, 26, 0.65);
            border: 1px solid rgba(251, 191, 36, 0.3);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow:
                0 8px 36px rgba(251, 191, 36, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.08);
            overflow: hidden;
        }}

        .podcast-hero::before {{
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 22px;
            padding: 2px;
            background: linear-gradient(135deg, var(--amber), var(--crimson), var(--teal));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
                    mask-composite: exclude;
            opacity: 0.45;
            pointer-events: none;
            animation: borderPulse 6s ease-in-out infinite;
        }}

        @keyframes borderPulse {{
            0%, 100% {{ opacity: 0.35; }}
            50%      {{ opacity: 0.7; }}
        }}

        .podcast-label {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            color: var(--crimson);
            letter-spacing: 0.2em;
            text-transform: uppercase;
            margin-bottom: 14px;
        }}

        .live-dot {{
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--crimson);
            box-shadow: 0 0 12px var(--crimson);
            animation: pulse 1.8s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50%      {{ opacity: 0.45; transform: scale(0.85); }}
        }}

        .podcast-title {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 2.1rem;
            font-weight: 900;
            line-height: 1.1;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #fff, var(--amber));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .podcast-sub {{
            color: var(--text-dim);
            margin-bottom: 24px;
            font-size: 1rem;
            max-width: 740px;
        }}

        .audio-shell {{
            display: flex;
            align-items: center;
            gap: 18px;
            padding: 14px 20px;
            background: rgba(6, 9, 18, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
        }}

        .visualizer {{
            display: flex;
            align-items: center;
            gap: 3px;
            height: 32px;
            flex-shrink: 0;
        }}

        .visualizer span {{
            display: block;
            width: 3px;
            background: linear-gradient(180deg, var(--amber), var(--crimson));
            border-radius: 2px;
            animation: bars 1.1s ease-in-out infinite;
        }}

        .visualizer span:nth-child(1) {{ height: 45%; animation-delay: 0.0s; }}
        .visualizer span:nth-child(2) {{ height: 85%; animation-delay: 0.12s; }}
        .visualizer span:nth-child(3) {{ height: 30%; animation-delay: 0.24s; }}
        .visualizer span:nth-child(4) {{ height: 95%; animation-delay: 0.36s; }}
        .visualizer span:nth-child(5) {{ height: 55%; animation-delay: 0.48s; }}

        @keyframes bars {{
            0%, 100% {{ transform: scaleY(0.4); }}
            50%      {{ transform: scaleY(1); }}
        }}

        audio {{
            flex: 1;
            min-width: 0;
            height: 40px;
        }}

        audio::-webkit-media-controls-panel {{ background: transparent; }}

        /* Summary */
        .summary {{
            padding: 22px 26px;
            border-radius: 14px;
            margin-bottom: 30px;
            background: rgba(10, 14, 26, 0.5);
            border: 1px solid rgba(59, 130, 246, 0.25);
            border-left: 3px solid var(--blue);
            backdrop-filter: blur(10px);
        }}

        .summary h2 {{
            font-size: 0.76rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--blue);
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .summary p {{
            font-size: 1.04rem;
            color: var(--text);
            line-height: 1.7;
        }}

        /* Content sections */
        .content-section {{
            padding: 26px 28px;
            border-radius: 16px;
            margin-bottom: 22px;
            background: rgba(10, 14, 26, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 22px rgba(0, 0, 0, 0.3);
            transition: border-color 0.4s, box-shadow 0.4s;
        }}

        .content-section:hover {{
            border-color: var(--accent);
            box-shadow: 0 8px 38px var(--accent-glow);
        }}

        .section-title {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 22px;
            color: #fff;
            letter-spacing: -0.01em;
        }}

        .section-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 36px; height: 36px;
            border-radius: 9px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--accent);
            font-size: 1.1rem;
            box-shadow: 0 0 14px var(--accent-glow);
        }}

        .section-items {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
        }}

        .content-item {{
            position: relative;
            padding: 20px 22px;
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 11px;
            transition: transform 0.3s ease, background 0.3s, border-color 0.3s, box-shadow 0.3s;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .content-item::before {{
            content: '';
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 2px;
            background: var(--accent);
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .content-item:hover {{
            transform: translateY(-3px);
            background: rgba(255, 255, 255, 0.04);
            border-color: var(--accent);
            box-shadow: 0 8px 26px var(--accent-glow);
        }}

        .content-item:hover::before {{ opacity: 1; }}

        .item-title {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 10px;
            line-height: 1.35;
        }}

        .item-insight {{
            color: var(--text-dim);
            font-size: 0.96rem;
            margin-bottom: 14px;
            line-height: 1.6;
            flex: 1;
        }}

        .item-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            padding-top: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 0.8rem;
            font-family: 'JetBrains Mono', monospace;
        }}

        .meta-source {{ color: var(--text-muted); }}

        .item-link {{
            color: var(--accent);
            text-decoration: none;
            transition: filter 0.2s, transform 0.2s;
        }}

        .item-link:hover {{
            filter: brightness(1.3);
            transform: translateX(3px);
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 40px 20px 10px;
            color: var(--text-muted);
            font-size: 0.85rem;
            font-family: 'JetBrains Mono', monospace;
        }}

        .footer a {{
            color: var(--amber);
            text-decoration: none;
            transition: color 0.2s;
        }}

        .footer a:hover {{ color: var(--crimson); }}

        .footer p {{ margin-bottom: 6px; }}

        .footer .signature {{ margin-top: 22px; opacity: 0.6; font-size: 0.78rem; }}

        /* Reveal on scroll */
        .reveal {{
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.7s ease, transform 0.7s ease;
        }}

        .reveal.visible {{
            opacity: 1;
            transform: translateY(0);
        }}

        @media (max-width: 700px) {{
            .container {{ padding: 16px; }}
            .header {{ padding: 14px 16px; flex-wrap: wrap; }}
            .header h1 {{ font-size: 1.2rem; }}
            .podcast-hero {{ padding: 26px 22px; }}
            .podcast-title {{ font-size: 1.6rem; }}
            .audio-shell {{ flex-wrap: wrap; }}
            .cursor-glow {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="grid-overlay"></div>
    <div class="lights"></div>
    <div class="cursor-glow"></div>

    <div class="container">
        <header class="header">
            <div class="brand">
                <div class="brand-mark">🌐</div>
                <div>
                    <h1>Global News Weekly</h1>
                    <div class="tagline">// international politics · every monday 06:00 UTC</div>
                </div>
            </div>
            <div class="date-badge">{week_str}</div>
        </header>

        <section class="podcast-hero reveal">
            <div class="podcast-label"><span class="live-dot"></span>this week's briefing</div>
            <h2 class="podcast-title">🎙️ Listen to the Briefing</h2>
            <p class="podcast-sub">AI-narrated summary of the week's most consequential international politics, conflict updates, and diplomatic developments — curated from BBC, Deutsche Welle, NYT, FT, Foreign Policy, and South China Morning Post.</p>
            <div class="audio-shell">
                <div class="visualizer" aria-hidden="true">
                    <span></span><span></span><span></span><span></span><span></span>
                </div>
                <audio controls preload="metadata">
                    <source src="audio/narration_{date_str}.mp3" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
        </section>

        <section class="summary reveal">
            <h2>// this week's overview</h2>
            <p>{weekly_summary}</p>
        </section>

        {sections_html}

        <footer class="footer">
            <p>// curated from BBC · Deutsche Welle · NYT · FT · Foreign Policy · SCMP</p>
            <p>auto-generated every monday at 06:00 UTC</p>
            <p style="margin-top: 16px;"><a href="https://github.com/EiriniOr/news-aggregation" target="_blank">view on github</a></p>
            <p class="signature">crafted by Eirini Ornithopoulou · for Meli, 2025</p>
        </footer>
    </div>

    <script>
        // Cursor-following glow
        const glow = document.querySelector('.cursor-glow');
        let glowX = window.innerWidth / 2, glowY = window.innerHeight / 2;
        let targetX = glowX, targetY = glowY;

        document.addEventListener('mousemove', (e) => {{
            targetX = e.clientX;
            targetY = e.clientY;
        }});

        function animateGlow() {{
            glowX += (targetX - glowX) * 0.1;
            glowY += (targetY - glowY) * 0.1;
            glow.style.left = glowX + 'px';
            glow.style.top  = glowY + 'px';
            requestAnimationFrame(animateGlow);
        }}
        animateGlow();

        // Reveal on scroll
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach((entry) => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }}
            }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.content-section, .summary, .podcast-hero').forEach((el) => {{
            el.classList.add('reveal');
            observer.observe(el);
        }});

        setTimeout(() => {{
            document.querySelectorAll('.podcast-hero, .summary').forEach((el) => el.classList.add('visible'));
        }}, 100);
    </script>
</body>
</html>
"""

        output_path = self.output_dir / "index.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print("✅ Webpage created successfully!")
        print(f"📁 Location: {output_path}")
        return output_path

    async def generate(self):
        """Main generation workflow"""
        print("🎯 Starting webpage generation...\n")
        curated_data = self.get_latest_curated_data()
        total_items = sum(
            len(items) for items in curated_data.get("sections", {}).values()
        )
        print(f"📊 Loaded curated content with {total_items} items\n")
        filepath = await self.create_webpage(curated_data)
        return filepath


async def main():
    generator = WebpageGenerator()
    filepath = await generator.generate()
    print(f"\n🎉 Done! Open your webpage:\n   {filepath}")


if __name__ == "__main__":
    asyncio.run(main())
