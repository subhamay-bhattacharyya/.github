#!/usr/bin/env python3

import os
import sys
import json
import re
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from urllib.parse import quote
from zoneinfo import ZoneInfo


def normalize_repo_url(value: str) -> str:
    """
    Normalize repository URL values that may already be wrapped in markdown links.
    """
    if not value:
        return ""

    raw = str(value).strip()
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw

    # Handle markdown-wrapped links like [repo](https://example.com)
    md_link_match = re.match(r"^\[[^\]]+\]\((https?://[^)]+)\)$", raw)
    if md_link_match:
        return md_link_match.group(1).strip()

    # Fall back to any URL found in the string.
    urls = re.findall(r"https?://[^\s)]+", raw)
    return urls[-1].rstrip("]") if urls else raw


def plain_text(value) -> str:
    """
    Convert markdown-like text into plain text for stable table rendering.
    """
    if value is None:
        return ""

    text = str(value)
    text = re.sub(r"!\[([^\]]*)\]\((https?://[^)]+)\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1", text)
    text = re.sub(r"[*_`~]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if text.lower() in {"not available", "n/a", "na"}:
        return "Not available"

    return text


def badge_label(value) -> str:
    """
    Encode badge labels safely for shields.io URLs.
    """
    text = plain_text(value)
    return quote(text.replace("-", "--")) if text else ""


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

    env.filters["repo_url"] = normalize_repo_url
    env.filters["plain_text"] = plain_text
    env.filters["badge_label"] = badge_label
    
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
        generated_at=est_time.strftime('%Y-%m-%d %H:%M:%S EST')
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
