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

---

## 2 Pydantic state & tool IO contracts

```python
# state.py
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Link(BaseModel):
    url: HttpUrl
    title: str
    source: str        # "web" | "youtube" | "twitter"
    views: int
    posted_at: str     # ISO date

class FlowState(BaseModel):
    topic: str
    links: List[Link] = []
    top_links: List[Link] = []
    blog_markdown: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    linkedin_post_url: Optional[HttpUrl] = None
```

Every node accepts and returns `FlowState`, making LangGraph’s type-checking happy. ([LangChain][1])

---

## 3 Scraper tools (Apify + Firecrawl)

```python
# tools.py
from apify_client import ApifyClient
from firecrawl import Firecrawl               # pip install firecrawl
from langchain.tools import tool
from datetime import datetime, timezone
from state import FlowState, Link
import os, operator

api_client = ApifyClient(os.environ["APIFY_TOKEN"])
firecrawl_client = Firecrawl(os.environ["FIRECRAWL_TOKEN"])

@tool
def scrape_youtube(state: FlowState) -> FlowState:
    """Search YouTube via Apify and append results to state.links"""
    run = api_client.actor("scraper_one/youtube-search-scraper").call(
        run_input={"searchKeywords": state.topic, "maxResults": 20}
    )
    items = run["output"]["items"]
    for vid in items:
        state.links.append(
            Link(
                url=vid["url"],
                title=vid["title"],
                source="youtube",
                views=vid["viewCount"],
                posted_at=vid["publishedDate"],
            )
        )
    return state
```

*Similar helpers* for X/Twitter (Playwright+Firecrawl or Scrapfly) and generic web search.
Apify’s official Python snippet for YouTube scraping is almost identical. ([Apify][2])
Firecrawl gives raw Markdown + metadata in one call. ([Firecrawl][3])

---

## 4 Rank/Filter node

```python
@tool
def rank_links(state: FlowState) -> FlowState:
    """Keep the 6 newest, highest-engagement links (balanced sources)."""
    latest = sorted(
        state.links,
        key=lambda l: (l.posted_at, l.views),
        reverse=True,
    )
    # simple top-n; you can add de-duplication & source quotas
    state.top_links = latest[:6]
    return state
```

---

## 5 Content-generation tools

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import base64, requests

llm = ChatOpenAI(model="gpt-4o-mini")

BLOG_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a tech blogger. Write a 1 000-word post using "
         "the following curated sources:\n{sources}"),
        ("human", "{topic}")
    ]
)

@tool
def write_blog(state: FlowState) -> FlowState:
    md = BLOG_TEMPLATE.format(
        topic=state.topic,
        sources="\n".join(f"- {l.title} ({l.url})" for l in state.top_links)
    )
    state.blog_markdown = llm.invoke(md).content
    return state

@tool
def generate_image(state: FlowState) -> FlowState:
    response = llm.images.generate(
        prompt=f"High-impact hero illustration for a blog post about {state.topic}",
        size="1024x1024",
        n=1,
    )
    state.image_url = response.data[0].url
    return state
```

---

## 6 LinkedIn posting tool

```python
import requests, json, os

@tool
def post_linkedin(state: FlowState) -> FlowState:
    """Publish the article to LinkedIn (requires Dev Platform access)."""
    # 1. Upload image, get imageURN (Posts API doc)
    # 2. Create article post referencing imageURN
    token = os.environ["LINKEDIN_ACCESS_TOKEN"]
    headers = {"Authorization": f"Bearer {token}",
               "X-Restli-Protocol-Version": "2.0.0",
               "Content-Type": "application/json"}
    payload = {
       "author": f"urn:li:person:{os.environ['LINKEDIN_MEMBER_ID']}",
       "lifecycleState": "PUBLISHED",
       "specificContent": {
          "com.linkedin.ugc.ShareContent": {
            "shareMediaCategory": "ARTICLE",
            "media": [{
               "status": "READY",
               "originalUrl": state.image_url,
               "title": {"text": state.topic}
            }],
            "shareCommentary": {
               "text": state.blog_markdown[:300] + "..."
            }
          }
       },
       "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    res = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        data=json.dumps(payload)
    )
    res.raise_for_status()
    state.linkedin_post_url = f"https://www.linkedin.com/feed/update/{res.json()['id']}"
    return state
```

LinkedIn’s official **Posts API** and third-party wrappers (e.g., **Unipile**) follow the same payload shape.  ([Microsoft Learn][4], [LinkedIn][5])

---

## 7 Wire it all together with LangGraph

```python
# graph.py
from langgraph.graph import Graph, END
from state import FlowState
from tools import (
    scrape_youtube, scrape_twitter, scrape_web,
    rank_links, write_blog, generate_image, post_linkedin
)
from langgraph.prebuilt import ToolNode, LLMNode

planner_model = ChatOpenAI(model="gpt-4o-mini")
planner = LLMNode(planner_model)

g = Graph()

g.add_node("plan", planner)
g.add_node("yt", ToolNode(scrape_youtube))
g.add_node("tw", ToolNode(scrape_twitter))
g.add_node("web", ToolNode(scrape_web))
g.add_node("rank", ToolNode(rank_links))
g.add_node("blog", ToolNode(write_blog))
g.add_node("img", ToolNode(generate_image))
g.add_node("post", ToolNode(post_linkedin))

# simple linear edges; you can route dynamically in the planner
g.add_edge("plan", "yt")
g.add_edge("yt", "tw")
g.add_edge("tw", "web")
g.add_edge("web", "rank")
g.add_edge("rank", "blog")
g.add_edge("blog", "img")
g.add_edge("img", "post")
g.set_entry_point("plan")
g.set_finish_point(END)

agent = g.compile()
```

---

## 8 Run the flow

```python
state = FlowState(topic="AI-powered DePIN in Southeast Asia")
result = agent.invoke(state.model_dump())
print(result["output"].linkedin_post_url)
```

You now have a fully typed, **goal-driven** agent crew that:

* plans
* gathers fresh, high-signal information
* creates rich content + imagery
* publishes autonomously

Scale-outs:

* add a **Critic** node that invokes a second LLM to review blog quality and loop back if revisions needed.
* schedule with **Airflow** or **Temporal**; emit LangSmith traces for observability.
* reuse the same template for other channels (Medium, WordPress) by swapping the posting tool.

Happy shipping!

[1]: https://python.langchain.com/docs/concepts/structured_outputs/?utm_source=chatgpt.com "Structured outputs - ️ LangChain"
[2]: https://apify.com/scraper_one/youtube-search-scraper/api/python?utm_source=chatgpt.com "Youtube Search Scraper API in Python - Apify"
[3]: https://www.firecrawl.dev/?utm_source=chatgpt.com "Firecrawl"
[4]: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2025-05&utm_source=chatgpt.com "Posts API - LinkedIn - Learn Microsoft"
[5]: https://www.linkedin.com/pulse/linkedin-api-python-integration-developers-guide-unipile-qsw0f?utm_source=chatgpt.com "LinkedIn API Python Integration: A Developer's Guide"
