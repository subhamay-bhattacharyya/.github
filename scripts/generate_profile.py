#!/usr/bin/env python3

import os
import sys
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from zoneinfo import ZoneInfo


def load_repos_data(json_file: str) -> dict:
    """
    Load repository data from JSON file.
    """
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(json_file, 'r') as f:
        return json.load(f)


def generate_profile_readme(repos_by_category: dict, template_name: str, output_file: str) -> None:
    """
    Generate profile README using Jinja2 template.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, '..', 'templates')
    
    # Create Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Load template
    template = env.get_template(template_name)
    
    # Get current time in EST
    est_time = datetime.now(ZoneInfo("America/New_York"))
    
    # Calculate total repositories across all categories
    total_repos = sum(len(repos) for repos in repos_by_category.values())
    
    # Render template
    html_content = template.render(
        repos_by_category=repos_by_category,
        total_repos=total_repos,
        generated_at=est_time.strftime('%H:%M:%S EST')
    )
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Write output
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Generated {output_file}")


def main() -> None:
    # Configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.join(script_dir, '..')
    
    json_file = os.path.join(repo_root, 'out', 'repos_by_category.json')
    template_name = "github_profile.html"
    output_file = os.path.join(repo_root, 'profile/README.md')
    
    print(f"📖 Reading data from {json_file}")
    repos_by_category = load_repos_data(json_file)
    
    print(f"🎨 Generating profile README")
    print(f"   - Categories: {len(repos_by_category)}")
    for category, repos in repos_by_category.items():
        print(f"   - {category}: {len(repos)} repositories")
    
    total_repos = sum(len(repos) for repos in repos_by_category.values())
    print(f"   - Total repositories: {total_repos}")
    
    generate_profile_readme(repos_by_category, template_name, output_file)


if __name__ == "__main__":
    main()
