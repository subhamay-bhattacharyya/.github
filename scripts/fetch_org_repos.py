#!/usr/bin/env python3

import os
import sys
import json
import requests
from typing import Dict, List
from pprint import pprint
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

GITHUB_API = "https://api.github.com"


def get_relative_time_with_color(dt: datetime) -> str:
    """
    Convert datetime to relative time string with color coding.
    Displays small, color-coded text on a new line.
    Color coding based on freshness:
    - Green: < 7 days
    - Yellow: 7-30 days
    - Orange: 30-90 days
    - Red: > 90 days
    """
    now = datetime.now(ZoneInfo("America/New_York"))
    diff = now - dt
    
    # Calculate time units
    seconds = diff.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = diff.days
    weeks = days // 7
    months = days // 30
    years = days // 365
    
    # Determine relative time string
    if seconds < 60:
        time_str = "just now"
    elif minutes < 60:
        count = int(minutes)
        time_str = f"{count} minute{'s' if count != 1 else ''} ago"
    elif hours < 24:
        count = int(hours)
        time_str = f"{count} hour{'s' if count != 1 else ''} ago"
    elif days < 7:
        count = days
        time_str = f"{count} day{'s' if count != 1 else ''} ago"
    elif weeks < 4:
        count = weeks
        time_str = f"{count} week{'s' if count != 1 else ''} ago"
    elif months < 12:
        count = months
        time_str = f"{count} month{'s' if count != 1 else ''} ago"
    else:
        count = years
        time_str = f"{count} year{'s' if count != 1 else ''} ago"
    
    # Determine flag color based on age
    if days < 7:
        color = "#22c55e"  # Green - very fresh
    elif days < 30:
        color = "#eab308"  # Yellow - recent
    elif days < 90:
        color = "#f97316"  # Orange - getting old
    else:
        color = "#ef4444"  # Red - stale
    
    return (
        f'<br><small title="{time_str}" '
        f'style="cursor: help; color: {color}; font-size: 0.65em;">'
        f'Updated {time_str}'
        f'</small>'
    )


def github_headers() -> Dict[str, str]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN is not set", file=sys.stderr)
        sys.exit(1)

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def fetch_all_repositories(org: str) -> List[Dict]:
    """
    Fetch all repositories in an organization (handles pagination).
    """
    repos: List[Dict] = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITHUB_API}/orgs/{org}/repos"
        params = {
            "per_page": per_page,
            "page": page,
            "type": "all",
        }

        resp = requests.get(url, headers=github_headers(), params=params)
        resp.raise_for_status()

        batch = resp.json()
        if not batch:
            break

        repos.extend(batch)
        page += 1

    return repos


def fetch_repo_custom_properties(org: str, repo: str) -> Dict[str, str]:
    """
    Fetch custom properties for a repository.
    Enterprise feature.
    """
    url = f"{GITHUB_API}/repos/{org}/{repo}/properties/values"
    resp = requests.get(url, headers=github_headers())

    if resp.status_code == 404:
        # Custom properties not enabled or not accessible
        return {}

    resp.raise_for_status()

    properties = {}
    for item in resp.json():
        properties[item["property_name"]] = item["value"]

    return properties


def fetch_branch_count(org: str, repo: str) -> int:
    """
    Fetch the number of branches for a repository.
    """
    url = f"{GITHUB_API}/repos/{org}/{repo}/branches"
    params = {"per_page": 100, "page": 1}
    
    resp = requests.get(url, headers=github_headers(), params=params)
    
    if resp.status_code == 404:
        return 0
    
    resp.raise_for_status()
    
    # Check if there are more pages
    branches = resp.json()
    total_count = len(branches)
    
    # If there's a Link header with pagination, we need to count all pages
    if 'Link' in resp.headers:
        page = 2
        while True:
            params["page"] = page
            resp = requests.get(url, headers=github_headers(), params=params)
            resp.raise_for_status()
            batch = resp.json()
            if not batch:
                break
            total_count += len(batch)
            page += 1
    
    return total_count


def main() -> None:
    # Support multiple organizations - can be comma-separated env var or default list
    orgs_env = os.getenv("GITHUB_ORGS")
    orgs_env = "subhamay-bhattacharyya,subhamay-bhattacharyya-gha, subhamay-bhattacharyya-tf"
    if orgs_env:
        orgs = [org.strip() for org in orgs_env.split(",")]
    else:
        orgs = ["subhamay-bhattacharyya"]  # Default organization(s)
    
    print(f"🔍 Fetching repositories for {len(orgs)} organization(s): {', '.join(orgs)}")
    
    # Dictionary to store repositories by ProjectCategory
    repos_by_category: Dict[str, List[Dict]] = {}

    for org in orgs:
        print(f"\n📂 Processing organization: {org}")
        repos = fetch_all_repositories(org)
        print(f"✅ Found {len(repos)} repositories in {org}\n")

        for repo in repos:
            name = repo["name"]
            print(f"📦 Processing repo: {org}/{name}")

            custom_props = fetch_repo_custom_properties(org, name)

            if custom_props.get("DisplayOnProfile") == "Yes":
                # Fetch branch count
                # pprint(repo)
                # break
                branch_count = fetch_branch_count(org, name)
                
                # Convert updated_at to relative time with color
                updated_at = repo.get("updated_at")
                if updated_at:
                    # Parse ISO 8601 timestamp and convert to EST
                    utc_time = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                    est_time = utc_time.astimezone(ZoneInfo("America/New_York"))
                    last_updated = get_relative_time_with_color(est_time)
                else:
                    last_updated = (
                        '<br><small title="N/A" '
                        'style="cursor: help; color: #6b7280; font-size: 0.65em;">'
                        'Updated N/A'
                        '</small>'
                    )
                
                repo_details = {
                    "name": name,
                    "html_url": repo.get("html_url"),
                    "description": repo.get("description"),
                    "status": custom_props.get("Status"),
                    "cloud_service_provider": "AWS" if custom_props.get("CloudServiceProvider") == "Amazon Web Service" else custom_props.get("CloudServiceProvider"),
                    "maturity": custom_props.get("Maturity"),
                    "notes": custom_props.get("Notes"),
                    "last_updated": last_updated,
                    "open_issues": repo.get("open_issues_count"),
                    "branches": branch_count,
                    "open_prs": repo.get("open_prs_count"),
                    "size_mb": f"{repo.get('size') / 1024:.2f} MB" if repo.get("size", 0) >= 1024 else f"{repo.get('size', 0)} KB"
                    }
                
                # Get the ProjectCategory, default to "Others" if not set
                project_category = custom_props.get("ProjectCategory", "Others")
                
                # Add repo to the appropriate category list
                if project_category not in repos_by_category:
                    repos_by_category[project_category] = []
                repos_by_category[project_category].append(repo_details)


    # Get the repository root (one level up from scripts directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.join(script_dir, '..')
    out_dir = os.path.join(repo_root, 'out')
    
    # Create out directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # Save the complete dictionary to repos_by_category.json
    output_file = os.path.join(out_dir, "repos_by_category.json")
    with open(output_file, "w") as f:
        json.dump(repos_by_category, f, indent=2)
    
    total_repos = sum(len(repos) for repos in repos_by_category.values())
    print(f"\n✅ Saved {total_repos} repositories across {len(repos_by_category)} categories to {output_file}")
    for category, repos_list in repos_by_category.items():
        print(f"   - {category}: {len(repos_list)} repositories")


if __name__ == "__main__":
    main()
