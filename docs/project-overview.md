# LinkedIn Content Automation Agent

A production-grade LangGraph system that automates LinkedIn content creation and publishing.

## Tech Stack

- **Core Framework**: LangGraph for orchestration
- **Data Validation**: Pydantic v2 for type-safe state management
- **AI Integration**: OpenAI GPT-4 for content generation
- **Data Collection**: 
  - Apify for YouTube scraping
  - Firecrawl for Twitter/X scraping
  - Custom web scraping

## Architecture

```
┌──────────┐      ┌─────────────┐
│ Planner  │──┐   │  ScrapeWeb  │──┐
└──────────┘  │   └─────────────┘  │
              │                    │
              │   ┌─────────────┐  │
              ├──▶│ ScrapeYT    │──┤
              │   └─────────────┘  │
              │                    │
              │   ┌─────────────┐  │
              ├──▶│ ScrapeX     │──┤
              │   └─────────────┘  │
              │                    ▼
              │          ┌─────────────────┐
              └─────────▶│  Rank/Filter    │
                         └─────────────────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │  WriteBlog      │
                         └─────────────────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │ GenerateImage   │
                         └─────────────────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │ PostLinkedIn    │
                         └─────────────────┘
```

## State Management

The system uses Pydantic models for type-safe state management:

- `ContentItem`: Individual content pieces from any source
- `ScrapedContent`: Collection of content from all sources
- `BlogPost`: Final blog post structure
- `AgentState`: Global state for the LangGraph system

## Project Structure

```
src/
├── config/         # Configuration management
├── graph/          # LangGraph workflow definitions
├── models/         # Pydantic models
├── services/       # External service integrations
└── utils/          # Utility functions
```

## Key Features

1. **Type-Safe State Management**
   - Pydantic models for all data structures
   - Runtime validation of all data
   - Clear separation of concerns

2. **Modular Architecture**
   - Each node is independently testable
   - Clear data flow between components
   - Easy to extend and modify

3. **Production-Ready**
   - Comprehensive logging
   - Environment-based configuration
   - Error handling and recovery