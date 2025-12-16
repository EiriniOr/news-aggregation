#!/usr/bin/env python3
"""
GitHub Deployment
Deploys the latest webpage to GitHub Pages
"""

import asyncio
import subprocess
from pathlib import Path
from datetime import datetime

class GitHubDeployer:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "output"
        self.output_dir.mkdir(exist_ok=True)

    async def deploy(self, html_path: str) -> bool:
        """Deploy webpage to GitHub Pages"""
        print("\n🚀 Deploying to GitHub Pages...")

        try:
            # Navigate to output directory
            subprocess.run(['git', 'init'], cwd=self.output_dir, check=True, capture_output=True)
            subprocess.run(['git', 'checkout', '-B', 'gh-pages'], cwd=self.output_dir, check=True, capture_output=True)

            # Add all files
            subprocess.run(['git', 'add', '.'], cwd=self.output_dir, check=True, capture_output=True)

            # Commit
            date_str = datetime.now().strftime('%Y-%m-%d')
            subprocess.run(
                ['git', 'commit', '-m', f'Update news digest - {date_str}'],
                cwd=self.output_dir,
                check=True,
                capture_output=True
            )

            # Note: Actual push would require repo configuration
            print(f"  ✓ Prepared for GitHub Pages deployment!")
            print(f"  📝 To deploy, configure your GitHub repository and push the output directory")
            print(f"     cd output && git push -f origin gh-pages")

            return True

        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Deployment preparation warning: {e}")
            return False
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            return False

async def deploy_to_github(html_path: str) -> bool:
    """Deploy webpage to GitHub Pages"""
    deployer = GitHubDeployer()
    return await deployer.deploy(html_path)

async def main():
    # Test deployment
    html_path = Path(__file__).parent.parent / "output" / "index.html"
    if html_path.exists():
        success = await deploy_to_github(str(html_path))
        if success:
            print("\n✅ Deployment preparation successful!")
        else:
            print("\n❌ Deployment preparation failed!")
    else:
        print(f"❌ HTML file not found: {html_path}")

if __name__ == "__main__":
    asyncio.run(main())
