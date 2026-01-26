#!/usr/bin/env python3
"""
Generate GitHub stats SVG using GitHub GraphQL API
Includes private repository statistics - ALL TIME
"""

import os
import requests
from datetime import datetime

# Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
USERNAME = 'j1d2'
OUTPUT_FILE = 'assets/github-stats.svg'

# Theme colors (tokyonight)
COLORS = {
    'bg': '#0f172a',
    'title': '#a78bfa',
    'text': '#e2e8f0',
    'icon': '#60a5fa',
    'stroke': '#2d3748'
}

def fetch_github_stats():
    """Fetch user stats from GitHub GraphQL API"""
    
    # Get account creation year for all-time commits
    user_query = """
    query($login: String!) {
      user(login: $login) {
        createdAt
        followers {
          totalCount
        }
        pullRequests {
          totalCount
        }
        issues {
          totalCount
        }
        openIssues: issues(states: OPEN) {
          totalCount
        }
        closedIssues: issues(states: CLOSED) {
          totalCount
        }
        contributionsCollection {
          contributionYears
        }
        repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC) {
          totalCount
          nodes {
            stargazerCount
          }
        }
      }
    }
    """
    
    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        'https://api.github.com/graphql',
        json={'query': user_query, 'variables': {'login': USERNAME}},
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"GraphQL query failed: {response.status_code} {response.text}")
    
    data = response.json()['data']['user']
    
    # Calculate total stars
    total_stars = sum(repo['stargazerCount'] for repo in data['repositories']['nodes'])
    
    # Get all contribution years
    years = data['contributionsCollection']['contributionYears']
    print(f"Fetching commits for years: {years}")
    
    # Fetch commits for each year to get all-time total
    total_commits = 0
    for year in years:
        year_query = f"""
        query($login: String!) {{
          user(login: $login) {{
            contributionsCollection(from: "{year}-01-01T00:00:00Z", to: "{year}-12-31T23:59:59Z") {{
              totalCommitContributions
              restrictedContributionsCount
            }}
          }}
        }}
        """
        
        year_response = requests.post(
            'https://api.github.com/graphql',
            json={'query': year_query, 'variables': {'login': USERNAME}},
            headers=headers
        )
        
        if year_response.status_code == 200:
            year_data = year_response.json()['data']['user']['contributionsCollection']
            year_commits = (
                year_data['totalCommitContributions'] +
                year_data['restrictedContributionsCount']
            )
            total_commits += year_commits
            print(f"  {year}: {year_commits} commits")
    
    # Calculate total issues (open + closed)
    total_issues = data['openIssues']['totalCount'] + data['closedIssues']['totalCount']
    
    print(f"\nIssue breakdown:")
    print(f"  Open: {data['openIssues']['totalCount']}")
    print(f"  Closed: {data['closedIssues']['totalCount']}")
    print(f"  Total: {total_issues}")
    
    return {
        'total_stars': total_stars,
        'total_commits': total_commits,
        'total_prs': data['pullRequests']['totalCount'],
        'total_issues': total_issues,
        'followers': data['followers']['totalCount']
    }

def generate_svg(stats):
    """Generate SVG with stats"""
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195">
  <defs>
    <style>
      .text {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {COLORS['text']} }}
      .stat {{ font: 600 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {COLORS['text']} }}
      .stat-value {{ font: 600 20px 'Segoe UI', Ubuntu, Sans-Serif; fill: {COLORS['text']} }}
      .bold {{ font-weight: 700 }}
      .icon {{ fill: {COLORS['icon']} }}
      .title {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {COLORS['title']} }}
    </style>
  </defs>
  
  <rect x="0.5" y="0.5" width="494" height="194" rx="4.5" fill="{COLORS['bg']}" stroke="{COLORS['stroke']}" stroke-opacity="0"/>
  
  <g transform="translate(25, 35)">
    <text class="title" x="0" y="0">{USERNAME}'s GitHub Stats</text>
    
    <!-- Total Stars -->
    <g transform="translate(0, 40)">
      <svg class="icon" x="0" y="-12" width="16" height="16" viewBox="0 0 16 16">
        <path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>
      </svg>
      <text class="stat" x="25" y="0">Total Stars:</text>
      <text class="stat-value bold" x="380" y="0" text-anchor="end">{stats['total_stars']:,}</text>
    </g>
    
    <!-- Total Commits -->
    <g transform="translate(0, 65)">
      <svg class="icon" x="0" y="-12" width="16" height="16" viewBox="0 0 16 16">
        <path d="M11.93 8.5a4.002 4.002 0 01-7.86 0H.75a.75.75 0 010-1.5h3.32a4.002 4.002 0 017.86 0h3.32a.75.75 0 010 1.5h-3.32zM8 6a2 2 0 100 4 2 2 0 000-4z"/>
      </svg>
      <text class="stat" x="25" y="0">Total Commits (All Time):</text>
      <text class="stat-value bold" x="380" y="0" text-anchor="end">{stats['total_commits']:,}</text>
    </g>
    
    <!-- Total PRs -->
    <g transform="translate(0, 90)">
      <svg class="icon" x="0" y="-12" width="16" height="16" viewBox="0 0 16 16">
        <path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z"/>
      </svg>
      <text class="stat" x="25" y="0">Total PRs:</text>
      <text class="stat-value bold" x="380" y="0" text-anchor="end">{stats['total_prs']:,}</text>
    </g>
    
    <!-- Total Issues -->
    <g transform="translate(0, 115)">
      <svg class="icon" x="0" y="-12" width="16" height="16" viewBox="0 0 16 16">
        <path d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"/>
        <path d="M8 0a8 8 0 110 16A8 8 0 018 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z"/>
      </svg>
      <text class="stat" x="25" y="0">Total Issues:</text>
      <text class="stat-value bold" x="380" y="0" text-anchor="end">{stats['total_issues']:,}</text>
    </g>
  </g>
  
  <text class="text" x="490" y="190" text-anchor="end" opacity="0.5" style="font-size: 10px">Updated: {datetime.utcnow().strftime('%Y-%m-%d')}</text>
</svg>'''
    
    return svg

def main():
    """Main execution"""
    print("Fetching GitHub stats...")
    stats = fetch_github_stats()
    print(f"\nFinal Stats: {stats}")
    
    print("\nGenerating SVG...")
    svg_content = generate_svg(stats)
    
    # Ensure assets directory exists
    os.makedirs('assets', exist_ok=True)
    
    # Write SVG file
    with open(OUTPUT_FILE, 'w') as f:
        f.write(svg_content)
    
    print(f"✓ Stats SVG generated: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
