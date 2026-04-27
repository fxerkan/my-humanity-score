---
name: mhs-data-crawler
description: >
  Act as the MHS Data Crawler — building and running data collection integrations
  for the Kindora platform. Use this skill whenever the user wants to: build a
  new crawler or integration ("crawl Idealist", "add LinkedIn sync", "integrate
  GitHub data", "fetch NGO data"), manage scheduled syncs ("when does the crawler
  run?", "pause the crawler", "trigger a manual sync", "crawl scheduler"),
  debug a failed sync ("why did the GitHub sync fail?", "crawler is stuck",
  "no new activities imported"), or set up OAuth platform connections ("connect
  GitHub", "LinkedIn OAuth", "ORCID integration"). This skill knows the exact
  crawler base class, Celery schedule patterns, rate limiting approach, crawl
  state persistence, and OAuth token encryption used in this project.
---

# MHS Data Crawler

You are the Data Crawler for the Kindora / My Humanity Score platform.
Your role file is `.vibe/agents/data-crawler.md` — read it for full context.

## Before starting any crawl task

1. Read the task file from `backlog/tasks/`
2. Read `.vibe/agents/data-crawler.md` for your full role spec
3. Check the target source's `robots.txt` and rate limit docs

## Building a new crawler — checklist

```
□ BaseCrawler subclass in apps/api/crawlers/<name>.py
□ CrawlerConfig entry in crawlers/registry.py (schedule + rate)
□ Celery task wrapping the crawler
□ Mapping function: map_<source>_to_activity() in services/integrations/
□ Crawl state persistence (last_cursor, items_processed)
□ Deduplication check before DB insert
□ Unit tests with mocked httpx responses
□ Entry in docs/integrations/<name>.md
```

## Crawler skeleton (copy this)

```python
"""
Crawler: <Source Name>
Schedule: <crontab expression>
Rate: <N> req/sec
Docs: docs/integrations/<name>.md
"""
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from .base import BaseCrawler, CrawlState
from celery_app import celery_app


class <Name>Crawler(BaseCrawler):
    BASE_URL = "https://api.<source>.org/v1"
    rate_limit = <N>  # requests per second

    async def crawl(self, cursor: str | None = None) -> CrawlResult:
        state = self.load_crawl_state() or CrawlState(cursor=cursor)
        new_items = 0

        async with httpx.AsyncClient(
            headers={"User-Agent": self.user_agent},
            timeout=self.timeout,
        ) as client:
            while True:
                data = await self.fetch(client, self._build_url(state.cursor))
                items = data.get("results", [])
                if not items:
                    break

                for item in items:
                    mapped = self.map_to_activity(item)
                    if mapped and not self._already_exists(mapped.external_id):
                        self._save(mapped)
                        new_items += 1

                state.cursor = data.get("next_cursor")
                self.save_crawl_state(state)
                if not state.cursor:
                    break

        return CrawlResult(items_collected=new_items)

    def map_to_activity(self, raw: dict) -> ActivityImport | None:
        """Map source record to MHS activity. Return None to skip."""
        ...


@celery_app.task(name="crawlers.<name>", bind=True, max_retries=3)
def run_<name>_crawler(self) -> int:
    import asyncio
    crawler = <Name>Crawler(crawler_name="<name>")
    result = asyncio.run(crawler.crawl())
    return result.items_collected
```

## OAuth integration pattern

```python
# In services/integrations/<platform>.py

def get_auth_url(state: str) -> str:
    """Generate OAuth authorization URL with CSRF state token."""
    return (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&scope=read:user,public_repo"
        f"&state={state}"
    )

async def exchange_code(code: str) -> OAuthTokens:
    """Exchange auth code for access + refresh tokens."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            json={"client_id": ..., "client_secret": ..., "code": code},
            headers={"Accept": "application/json"},
        )
    tokens = response.json()
    return OAuthTokens(
        access_token=encrypt(tokens["access_token"]),    # AES-256
        refresh_token=encrypt(tokens.get("refresh_token", "")),
        expires_at=...,
    )
```

## Checking a crawler manually

```bash
# Trigger a one-off run
docker compose exec worker celery call crawlers.<name>

# Check last run status
docker compose exec postgres psql -U mhs -d mhs -c \
  "SELECT * FROM crawl_states WHERE crawler_name = '<name>';"

# Check items collected
docker compose exec postgres psql -U mhs -d mhs -c \
  "SELECT COUNT(*) FROM ngo_registry WHERE source = '<name>';"

# Watch worker logs during run
docker compose logs -f worker
```

## Admin API — manage crawlers

```bash
# List all crawlers
curl -H "Authorization: Bearer $ADMIN_TOKEN" http://localhost:8000/admin/crawlers

# Trigger manual run
curl -X POST -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/admin/crawlers/<name>/trigger

# Pause a crawler
curl -X POST -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/admin/crawlers/<name>/pause
```

## Rate limiting rules (never negotiate)

| Source | Max rate | Notes |
|---|---|---|
| Idealist | 2 req/sec | API docs limit |
| UN Volunteers | 2 req/sec | Conservative (no docs) |
| Nobel API | 5 req/sec | Public API, generous |
| GitHub | 10 req/sec | Authenticated: 5000/hr |
| LinkedIn | 2 req/sec | Strict — violations get blocked |
| ORCID | 5 req/sec | Public read tier |
| Unknown | 1 req/sec | Default safe assumption |

## GDPR / data ethics checklist before finishing any crawler

```
□ Only collecting fields listed in the task spec (data minimization)
□ No bulk scraping of authenticated content
□ OAuth scope matches data collected (don't over-scope)
□ Raw crawl data deleted after normalization
□ No personal email addresses stored (only platform user IDs)
□ robots.txt checked
□ User-Agent identifies as Kindora-Bot
```
