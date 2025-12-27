# International Politics Weekly Digest

Automatically generates a **professional news website** with **AI-narrated audio** every week featuring the latest updates in **international politics**, **war and conflict**, and **diplomacy**.

## What It Does

Every Monday at 6:00 AM UTC, this fully automated system:

1. **Collects** news via RSS feeds from major international sources (BBC, Deutsche Welle, New York Times, Financial Times, Foreign Policy, South China Morning Post)
2. **Curates** content using Claude AI to filter and categorize by relevance and significance
3. **Generates** a professional multi-column news webpage
4. **Creates** AI-narrated audio summary with OpenAI TTS
5. **Deploys** everything to GitHub Pages

## How It Works (No Google Search)

This system uses **RSS feeds**, not web scraping or Google Search:
- RSS = structured XML feeds that news sites publish automatically
- Free, reliable, no API keys needed for collection
- Direct from source (BBC, NYT, etc.)
- `feedparser` library parses the XML into Python objects

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/rena/news-aggregation
pip3 install anthropic requests feedparser openai
```

**Note**: On macOS with Homebrew Python, you may need to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Your API Keys

You need API keys for:
- **Anthropic Claude** (content curation)
- **OpenAI** (AI voice narration)

```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"
```

Or add to your `~/.zshrc` or `~/.bash_profile`:

```bash
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.zshrc
echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Test It Manually

Run the full pipeline once to make sure everything works:

```bash
python3 generate_weekly_digest.py
```

This will:
- Collect news from the past week
- Curate with Claude
- Generate a professional webpage
- Create AI-narrated audio (if OpenAI key is set)
- Prepare for GitHub Pages deployment

**Expected outputs**:
- Webpage: `output/index.html`
- Audio: `output/audio/narration_YYYYMMDD.mp3`
- Archive pages for previous weeks

### 4. Set Up Automation

#### Option A: GitHub Actions (Recommended - Free & Cloud-based)

The system is already configured to run automatically via GitHub Actions!

**Setup steps:**

1. **Create a new GitHub repository** for this project
2. **Push the code** to your repository:
   ```bash
   cd /Users/rena/news-aggregation
   git init
   git add .
   git commit -m "Initial commit: Global News Weekly"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/news-aggregation.git
   git push -u origin main
   ```

3. **Add GitHub Secrets**:
   Go to: `https://github.com/YOUR_USERNAME/news-aggregation/settings/secrets/actions`

   Add these secrets:
   - `ANTHROPIC_API_KEY`: Your Claude API key
   - `OPENAI_API_KEY`: Your OpenAI API key

4. **Enable GitHub Pages**:
   - Go to Settings > Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` / `root`
   - Save

5. **That's it!** The workflow runs automatically every Monday at 6:00 AM UTC.

6. **Manual trigger** (optional):
   - Go to Actions tab
   - Click "Generate Weekly News Digest"
   - Click "Run workflow"

**What happens:**
- Runs in GitHub's cloud (free for public repos)
- Generates webpage + audio
- Deploys to GitHub Pages automatically
- No local machine needed!

#### Option B: Manual Run

If you prefer manual control, just run this command whenever you want your digest:

```bash
cd /Users/rena/news-aggregation
python3 generate_weekly_digest.py
```

## News Sources (RSS Feeds)

- **BBC World** - British Broadcasting Corporation world news
- **Deutsche Welle** - German international broadcaster
- **New York Times World** - US newspaper of record
- **Financial Times** - Global business/politics coverage
- **Foreign Policy** - International affairs analysis
- **South China Morning Post** - Asian perspective

## Content Categories

### International Politics
Major diplomatic developments, elections, policy changes, government actions

### War & Conflict
Military operations, conflicts, peace negotiations, security developments

### Diplomacy & Relations
International relations, treaties, summits, bilateral agreements

## How It Works

### Architecture

```
┌─────────────────┐
│ RSS Feed Sources│
│ • BBC World     │
│ • Deutsche Welle│
│ • NYT World     │
│ • Financial Times│
│ • Foreign Policy│
│ • SCMP          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ collect_news.py │  Aggregates all sources
│                 │  Saves: data/raw_news_*.json
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ curate_content  │  Claude filters & categorizes
│      .py        │  Saves: data/curated_*.json
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ generate_       │  Creates professional HTML
│ webpage.py      │  Multi-column news layout
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ generate_       │  OpenAI TTS narration
│ audio.py        │  Professional news voice
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ deploy_github   │  GitHub Pages deployment
│      .py        │  Live website
└─────────────────┘
```

### Data Flow

1. **Collection**: Pulls recent articles from RSS feeds
2. **Storage**: Saves raw JSON data to `data/` directory
3. **Curation**: Claude analyzes articles and selects the most significant
4. **Generation**: Creates professional HTML with multi-column layout
5. **Audio**: Generates narrated summary of key stories
6. **Deployment**: Publishes to GitHub Pages

## File Structure

```
news-aggregation/
├── generate_weekly_digest.py      # Main orchestrator
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
│
├── .github/
│   └── workflows/
│       └── weekly-digest.yml      # GitHub Actions workflow
│
├── scripts/
│   ├── collect_news.py            # RSS feed collector
│   ├── curate_content.py          # Claude curation
│   ├── generate_webpage.py        # HTML generation
│   ├── generate_audio.py          # Audio narration
│   └── deploy_github.py           # GitHub deployment
│
├── data/
│   ├── raw_news_*.json            # Collected articles
│   └── curated_*.json             # Curated content
│
├── output/
│   ├── index.html                 # Main webpage
│   ├── digest-*.html              # Archive pages
│   └── audio/
│       ├── narration_*.mp3        # Audio files
│       └── script_*.json          # Narration scripts
│
└── logs/
    ├── stdout.log                 # Process logs
    └── stderr.log                 # Error logs
```

## Commands Reference

### Run Full Pipeline

```bash
python3 generate_weekly_digest.py
```

### Run Individual Steps

```bash
# Step 1: Collect news
cd scripts && python3 collect_news.py

# Step 2: Curate content (requires Step 1)
cd scripts && python3 curate_content.py

# Step 3: Generate webpage (requires Step 2)
cd scripts && python3 generate_webpage.py

# Step 4: Generate audio (requires Step 2)
cd scripts && python3 generate_audio.py

# Step 5: Deploy to GitHub Pages (requires Steps 3-4)
cd scripts && python3 deploy_github.py
```

## Design Features

### Professional News Website Style
- Clean, readable typography (Georgia serif font)
- Multi-column grid layout for easy scanning
- Navy blue and grey color scheme
- Responsive design for mobile and desktop
- Category color coding for quick identification

### Audio Narration
- Professional broadcaster tone
- 2-3 minute summary of key stories
- High-quality OpenAI TTS voice
- Embedded audio player on webpage

### Archive System
- Automatic archive pages for previous weeks
- Navigation between current and past editions
- Preserves full content history

## Customization

### Change Schedule

Edit `.github/workflows/weekly-digest.yml`:

```yaml
schedule:
  # Run every Friday at 18:00 UTC
  - cron: '0 18 * * 5'
```

### Add/Remove News Sources

Edit `scripts/collect_news.py`:

```python
self.feeds = {
    'your_source': 'https://example.com/rss',
    # Add more sources...
}
```

### Modify Categories

Edit `scripts/curate_content.py` to change the categorization prompt and section names.

### Change Design

Edit `scripts/generate_webpage.py` to modify:
- Color scheme (CSS variables)
- Layout (grid columns, spacing)
- Typography (fonts, sizes)
- Section ordering

### Change Audio Voice

Edit `scripts/generate_audio.py`:

```python
voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
```

## Troubleshooting

### "No curated data found"

Run the pipeline in order:

```bash
cd scripts
python3 collect_news.py
python3 curate_content.py
cd ..
python3 generate_weekly_digest.py
```

### API Key Not Found

Make sure environment variables are set:

```bash
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
```

If empty, export them:

```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
```

### No Articles Collected

- Check internet connection
- Verify RSS feeds are accessible
- Try increasing the lookback period in `collect_news.py`
- Check `logs/` directory for errors

### GitHub Actions Not Running

- Verify secrets are set correctly in repository settings
- Check Actions tab for error messages
- Ensure GitHub Pages is enabled
- Check workflow file syntax

## Cost Estimate

### Claude API (Anthropic)
- ~$0.05-0.10 per week for content curation
- Depends on number of articles collected

### OpenAI TTS
- ~$0.10-0.15 per week for audio generation
- Based on script length (2-3 minutes)

### GitHub
- **Free** for public repositories
- Includes Actions minutes and Pages hosting

**Total: ~$0.15-0.25 per week or ~$10-13 per year**

## Future Enhancements

Possible additions:
- Email delivery of weekly digest
- RSS feed for the digest itself
- Social media auto-posting
- Sentiment analysis of news trends
- Interactive charts and data visualizations
- Newsletter subscription system
- PDF export option
- Multi-language support

## FAQ

**Q: How much does this cost?**
A: Approximately $0.15-0.25 per week for API usage. GitHub hosting is free.

**Q: Can I change the schedule?**
A: Yes, edit the cron schedule in `.github/workflows/weekly-digest.yml`.

**Q: What if I miss a week?**
A: The system always looks at the past 7 days, so you can run it anytime.

**Q: Can I add more news sources?**
A: Yes, add RSS feed URLs to the `feeds` dictionary in `collect_news.py`.

**Q: How do I customize the design?**
A: Edit the CSS in `generate_webpage.py` to change colors, fonts, and layout.

**Q: Can I run this locally without GitHub?**
A: Yes, just run `python3 generate_weekly_digest.py` and open `output/index.html`.

## Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Verify API keys are set correctly
3. Test components individually
4. Review error messages in GitHub Actions

## License

Personal use project. Modify as needed!

---

**Status**: Ready to use

**Next Steps**:
1. Install dependencies
2. Set API keys
3. Run test generation
4. Push to GitHub
5. Configure GitHub Actions
6. Enable automation

Stay informed with Global News Weekly!
