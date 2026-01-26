# GitHub Profile Repository - j1d2

## Repository Context

This is JD's GitHub profile repository (j1d2/j1d2) - a special repository that displays on the GitHub profile page at https://github.com/j1d2.

## About JD

- **Role**: Principal Engineer specializing in Cloud, Data & AI Systems
- **Experience**: 15+ years turning complex challenges into elegant solutions
- **Expertise**: Serverless architectures, Kubernetes, CI/CD automation, multi-cloud environments, AI-driven workflows
- **Tech Focus**: Claude, Copilot, Gemini, AWS, GCP, Azure, Python, Go, Rust
- **Portfolio**: https://j1d2.me
- **Email**: myself@j1d2.me

## Repository Structure

- `README.md` - Main profile content displayed on GitHub profile page
- `.github/` - GitHub-specific configurations and instructions
  - `copilot-instructions.md` - This file with context for Copilot
  - `workflows/update-stats.yml` - Daily GitHub Action to update stats
  - `scripts/generate-stats.py` - Python script for generating custom stats SVG
- `assets/` - Generated assets
  - `github-stats.svg` - Auto-generated stats card (commits, PRs, issues)

## Content Guidelines

### Tone & Style
- Professional yet approachable
- Technical but accessible
- Showcase expertise without being overly promotional
- Use clear, concise language

### Visual Design
- Maintain clean, organized layout with proper alignment
- Use badges consistently (style=flat-square or style=for-the-badge)
- Keep color scheme cohesive (current theme: purple/blue tones with dark background)
- Ensure sections are well-spaced and easy to scan

### Technical Accuracy
- Keep tech stack current and relevant
- Only include technologies actively used or explored
- Ensure all links are functional
- Update activity graphs and stats as needed

## Key Sections to Maintain

1. **Header** - Name, title, tagline with portfolio/GitHub badges
2. **About Me** - Brief professional summary
3. **What I Do** - Core competencies in table format
4. **Tech Stack** - Categorized badges for technologies
5. **Tech Expertise** - Detailed table of capabilities
6. **Highlights** - Key achievements and accomplishments
7. **Currently Exploring** - Active learning/research areas
8. **Let's Connect** - Contact information and links

## Update Principles

- **Minimal changes**: Only modify what's necessary
- **Consistency**: Match existing formatting and style
- **Accuracy**: Verify all new information before adding
- **Links**: Test all URLs before committing
- **Badges**: Use shields.io for consistency (https://shields.io)

## Common Tasks

### Adding New Technology
1. Add badge to appropriate Tech Stack section
2. Update Tech Expertise table if major technology
3. Consider adding to "Currently Exploring" if newly learning

### Updating Highlights
- Keep to 4-6 bullet points
- Focus on quantifiable achievements
- Use action verbs (Architected, Pioneered, Led, Built, Automated)

### Refreshing Content
- Update "Currently Exploring" section regularly
- Verify external service URLs (badges, graphs) are working
- Keep year counts accurate (e.g., "15+ years")

## External Dependencies

- **Badges**: shields.io
- **Activity Graph**: github-readme-activity-graph.vercel.app
- **Visitor Counter**: komarev.com/ghpvc

## Custom Stats Implementation

The profile uses a **custom GitHub stats card** generated daily via GitHub Actions:

### How It Works
1. **Workflow**: `.github/workflows/update-stats.yml` runs daily at midnight UTC (or manually via workflow_dispatch)
2. **Script**: `.github/scripts/generate-stats.py` uses GitHub GraphQL API to:
   - Query all contribution years for accurate all-time commit counts
   - Fetch PRs and issues from all repositories (public + private)
   - Generate SVG with tokyonight theme colors
3. **Output**: Updates `assets/github-stats.svg` and commits automatically

### Authentication
- Uses fine-grained Personal Access Token stored as `STATS_TOKEN` secret
- Required permissions (all read-only):
  - Contents
  - Metadata
  - Issues
  - Pull requests
- Token securely accesses private repos without exposing specific details

### Why Custom?
- **Privacy**: Shows aggregate stats from private repos without exposing sensitive data
- **Accuracy**: Direct GraphQL queries ensure correct all-time statistics
- **Control**: No dependency on third-party services or Vercel instances
- **Security**: Runs in our own GitHub Actions with encrypted secrets

### Current Stats (as of last run)
- 909 commits (all-time)
- 201 PRs (across j1d2me-web, crabby_crypto_lake, j1d2, iamsam)
- 127 issues (across multiple repos)

### Maintenance
- Stats update automatically daily - no manual intervention needed
- If PAT expires, create new fine-grained token with same minimal permissions
- SVG is committed by `github-actions[bot]` - bypasses branch protection

## Notes

- This README is public-facing and represents professional brand
- Changes should enhance credibility and showcase expertise
- Avoid trendy/temporary content that dates quickly
- Keep mobile-friendly (GitHub renders on all devices)
