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


def generate_profile_readme(data: dict, template_name: str, output_file: str) -> None:
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
    
    # Render template
    html_content = template.render(
        org=data.get('org'),
        repositories=data.get('repositories', []),
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
    
    json_file = os.path.join(repo_root, 'out', 'repos_data.json')
    template_name = "github_profile.html"
    output_file = os.path.join(repo_root, 'README.md')
    
    print(f"📖 Reading data from {json_file}")
    data = load_repos_data(json_file)
    
    print(f"🎨 Generating profile README")
    print(f"   - Organization: {data.get('org')}")
    print(f"   - Repositories: {len(data.get('repositories', []))}")
    
    generate_profile_readme(data, template_name, output_file)


if __name__ == "__main__":
    main()
