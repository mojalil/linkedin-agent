# LinkedIn Content Automation Agent

An AI-powered agent that automatically creates and publishes LinkedIn content using LangGraph.

## Features

- Automated content discovery from YouTube, Twitter/X, and web sources
- Content ranking and filtering
- Blog post generation
- Image generation
- LinkedIn integration for automated posting

## Requirements

- Python 3.9+
- Poetry for dependency management

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Set up environment variables:
   ```bash
   APIFY_TOKEN=your_apify_token
   FIRECRAWL_TOKEN=your_firecrawl_token
   LINKEDIN_ACCESS_TOKEN=your_linkedin_token
   LINKEDIN_MEMBER_ID=your_linkedin_member_id
   OPENAI_API_KEY=your_openai_api_key
   ```

## Project Structure

```
linkedin-agent/
├── docs/
│   ├── project-overview.md
│   └── project-planning.md
├── src/
│   ├── __init__.py
│   ├── state.py
│   ├── tools.py
│   ├── graph.py
│   └── config.py
├── tests/
│   └── __init__.py
├── pyproject.toml
└── README.md
```

## Development

This project uses Poetry for dependency management. To add new dependencies:

```bash
poetry add package-name
```

## License

MIT
