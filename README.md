# LinkedIn Content Automation Agent

An AI-powered agent system that automatically creates and publishes LinkedIn content using PydanticAI for agent development and LangGraph for workflow orchestration.

## Tech Stack

- **Agent Framework**: PydanticAI
  - Type-safe agent definitions
  - Structured tool schemas
  - Built-in validation
- **Workflow Orchestration**: LangGraph
  - State management
  - Control flow
  - Error handling
- **AI Integration**: OpenAI GPT-4 for content generation
- **Data Collection**: 
  - Apify for YouTube scraping
  - Firecrawl for Twitter/X scraping
  - Custom web scraping

## Features

- Type-safe agent development with PydanticAI
- Robust workflow orchestration with LangGraph
- Automated content discovery from multiple sources
- Content ranking and filtering
- AI-powered blog post generation
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
3. Set up environment variables in `.env`:
   ```bash
   APIFY_TOKEN=your_apify_token
   FIRECRAWL_TOKEN=your_firecrawl_token
   LINKEDIN_ACCESS_TOKEN=your_linkedin_token
   LINKEDIN_MEMBER_ID=your_linkedin_member_id
   OPENAI_API_KEY=your_openai_api_key
   ```

## Project Structure

```
src/
├── agents/                 # PydanticAI agent definitions
│   ├── base/              # Base agent and common tools
│   │   ├── schema.py      # Base agent schemas
│   │   ├── tools.py       # Common tools
│   │   └── errors.py      # Error handling
│   ├── scrapers/          # Content discovery agents
│   │   ├── youtube.py     # YouTube scraper agent
│   │   ├── twitter.py     # Twitter scraper agent
│   │   └── web.py         # Web scraper agent
│   ├── processors/        # Content processing agents
│   │   ├── ranker.py      # Content ranking agent
│   │   ├── writer.py      # Blog writer agent
│   │   └── image.py       # Image generator agent
│   └── linkedin/          # LinkedIn integration
│       ├── agent.py       # LinkedIn posting agent
│       └── tools.py       # LinkedIn API tools
├── graph/                 # LangGraph workflow definitions
│   ├── nodes/            # Workflow nodes
│   ├── edges.py          # Node connections
│   └── state.py          # Workflow state
├── models/               # Pydantic models
│   ├── content.py        # Content models
│   ├── blog.py          # Blog post models
│   └── linkedin.py      # LinkedIn models
├── services/            # External service integrations
│   ├── apify.py         # Apify client
│   ├── firecrawl.py     # Firecrawl client
│   └── openai.py        # OpenAI client
└── utils/               # Utility functions
    ├── logging.py       # Logging setup
    └── config.py        # Configuration management
```

## Development

This project uses Poetry for dependency management. To add new dependencies:

```bash
poetry add package-name
```

## Current Status

- ✅ Core infrastructure setup
- ✅ Basic LangGraph workflow
- ✅ Pydantic models
- ✅ Configuration management
- ✅ Logging system
- 🔄 Agent development (in progress)

## License

MIT
