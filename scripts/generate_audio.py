#!/usr/bin/env python3
"""
Audio Generator - International Politics & Swedish News
Creates AI-narrated audio from curated news
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import anthropic
import os

class AudioGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.audio_dir = self.output_dir / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)

        self.claude_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def get_latest_curated_data(self):
        """Load most recent curated content"""
        data_files = sorted(self.data_dir.glob("curated_*.json"), reverse=True)

        if not data_files:
            raise FileNotFoundError("No curated data found")

        with open(data_files[0], encoding='utf-8') as f:
            return json.load(f)

    async def generate_script(self, curated_data):
        """Generate narration script using Claude"""
        print("📝 Generating narration script with Claude...")

        sections = curated_data.get('sections', {})

        prompt = f"""Create a natural, professional 2-3 minute audio script about this week's international politics and Swedish news.

Style:
- Professional news broadcaster tone
- Clear, articulate delivery
- Short, impactful sentences
- Natural transitions between topics
- Time: approximately 2-3 minutes total

Content to cover:
Weekly Summary: {curated_data.get('weekly_summary', '')}

International Politics ({len(sections.get('International Politics', []))} items):
{json.dumps(sections.get('International Politics', [])[:3], indent=2, ensure_ascii=False)}

War & Conflict ({len(sections.get('War & Conflict', []))} items):
{json.dumps(sections.get('War & Conflict', [])[:3], indent=2, ensure_ascii=False)}

Swedish News ({len(sections.get('Swedish News', []))} items):
{json.dumps(sections.get('Swedish News', [])[:3], indent=2, ensure_ascii=False)}

Diplomacy & Relations ({len(sections.get('Diplomacy & Relations', []))} items):
{json.dumps(sections.get('Diplomacy & Relations', [])[:3], indent=2, ensure_ascii=False)}

Output as JSON with sections for timing:
{{
  "intro": "Hook and welcome (5-10 seconds)",
  "summary": "Weekly overview (15-20 seconds)",
  "international": "International politics highlights - mention top 2-3 stories (30-40 seconds)",
  "conflict": "War and conflict updates - mention top 2-3 stories (30-40 seconds)",
  "swedish": "Swedish news - mention top 2-3 stories (25-35 seconds)",
  "diplomacy": "Diplomacy highlights - mention top 2 stories (20-30 seconds)",
  "outro": "Sign-off (10 seconds)"
}}

Focus on the most significant developments. Keep it authoritative and informative."""

        message = self.claude_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2500,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        response_text = message.content[0].text

        # Try to find JSON in the response
        try:
            # Look for JSON block
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif response_text.strip().startswith('{'):
                # Try to parse directly
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                response_text = response_text[json_start:json_end]

            script = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback to simple script
            script = {
                "intro": f"Welcome to Global News Weekly for {datetime.now().strftime('%B %d, %Y')}. Your digest of international politics, conflict analysis, and Swedish news.",
                "summary": curated_data.get('weekly_summary', ''),
                "international": f"This week in international politics, we saw {len(sections.get('International Politics', []))} major developments.",
                "conflict": f"On the conflict front, {len(sections.get('War & Conflict', []))} important updates.",
                "swedish": f"In Swedish news, {len(sections.get('Swedish News', []))} significant stories.",
                "diplomacy": f"And in diplomacy, {len(sections.get('Diplomacy & Relations', []))} notable developments.",
                "outro": "That's your Global News Weekly. For full details, visit the link below."
            }

        # Save script
        date_str = datetime.now().strftime('%Y%m%d')
        script_path = self.audio_dir / f"script_{date_str}.json"
        with open(script_path, 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Script saved: {script_path}")
        return script

    async def generate_audio(self, script):
        """Generate audio narration using OpenAI TTS"""
        print("🎙️  Generating audio narration with OpenAI TTS...")

        try:
            from openai import OpenAI
            openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

            # Combine all script sections
            full_script = "\n\n".join([
                script.get('intro', ''),
                script.get('summary', ''),
                script.get('international', ''),
                script.get('conflict', ''),
                script.get('swedish', ''),
                script.get('diplomacy', ''),
                script.get('outro', '')
            ])

            # Generate audio
            response = openai_client.audio.speech.create(
                model="tts-1-hd",
                voice="onyx",  # Professional male voice for news
                input=full_script
            )

            # Save audio file
            date_str = datetime.now().strftime('%Y%m%d')
            audio_path = self.audio_dir / f"narration_{date_str}.mp3"
            response.stream_to_file(str(audio_path))

            print(f"  ✓ Audio saved: {audio_path}")
            return audio_path

        except ImportError:
            print("  ⚠️  OpenAI package not installed - audio generation skipped")
            return None
        except Exception as e:
            print(f"  ⚠️  Audio generation failed: {e}")
            return None

    async def generate(self):
        """Main audio generation workflow"""
        print("🎙️  Starting audio generation...\n")

        try:
            # Load curated data
            curated_data = self.get_latest_curated_data()

            # Generate script
            script = await self.generate_script(curated_data)

            # Generate audio
            audio_path = await self.generate_audio(script)

            if audio_path:
                print(f"\n✅ Audio generation complete: {audio_path}")
            else:
                print("\n⚠️  Audio generation skipped")

            return audio_path

        except Exception as e:
            print(f"\n❌ Audio generation failed: {e}")
            return None

async def main():
    generator = AudioGenerator()
    audio_path = await generator.generate()

    if audio_path:
        print(f"\n🎉 Audio ready: {audio_path}")

if __name__ == "__main__":
    asyncio.run(main())
