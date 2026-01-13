#!/usr/bin/env python3

import os
import sys
import json
import requests
from typing import Dict, List
from pprint import pprint
from datetime import datetime
from zoneinfo import ZoneInfo

GITHUB_API = "https://api.github.com"


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


def main() -> None:
    org = "subhamay-bhattacharyya" #os.getenv("GITHUB_ORG")
    if not org:
        print("❌ org is not set", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Fetching repositories for org: {org}")
    repos = fetch_all_repositories(org)

    print(f"✅ Found {len(repos)} repositories\n")

    results = []

    for repo in repos:
        name = repo["name"]
        print(f"📦 Processing repo: {name}")

        custom_props = fetch_repo_custom_properties(org, name)

        if custom_props.get("DiaplayOnProfile") == "Yes":
            # Convert updated_at to EST time
            updated_at = repo.get("updated_at")
            if updated_at:
                # Parse ISO 8601 timestamp and convert to EST
                utc_time = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                est_time = utc_time.astimezone(ZoneInfo("America/New_York"))
                last_updated = est_time.strftime('%H:%M:%S EST')
            else:
                last_updated = None
            
            results.append({
            "name": name,
            "description": repo.get("description"),
            "status": custom_props.get("Status"),
            "last_updated": last_updated,
            "open_issues": repo.get("open_issues_count"),
            "open_prs": repo.get("open_prs_count"),
            "size_mb": repo.get("size")
            })

    # Get the repository root (one level up from scripts directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.join(script_dir, '..')
    out_dir = os.path.join(repo_root, 'out')
    
    # Create out directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # Save results to JSON file in out directory
    output_file = os.path.join(out_dir, "repos_data.json")
    with open(output_file, "w") as f:
        json.dump({"org": org, "repositories": results}, f, indent=2)
    
    print(f"\n✅ Saved {len(results)} repositories to {output_file}")



if __name__ == "__main__":
    main()
