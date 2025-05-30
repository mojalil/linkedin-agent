Below is a **production-grade blueprint** (plus runnable code skeleton) for a *goal-driven* LangGraph crew that:

1. Takes a **topic** as input
2. Finds *fresh, high-engagement* content on the open web, YouTube and X/Twitter (via **Apify** + **Firecrawl**)
3. Writes a long-form blog post and generates a hero image
4. Auto-posts it to LinkedIn

Everything is typed with **Pydantic** models so each node knows exactly what data it receives and returns.

---

## 1 Agent-team architecture

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

*Planner* keeps the **goal** (“publish a LinkedIn post on *X*”) in global state, delegates subtasks, and decides when to finish.

## Project Structure

```
src/config
src/graph
src/models
src/services
src/utils
```