---
id: TASK-39
assignee: []
title: "Crawl Scheduler + Rate Limiter"
status: To Do
priority: medium
labels: ["epic009-platform-integrations", "gemini-pro", "data-crawler"]
dependencies:
  - task-38
  - task-20
acceptance_criteria:
  - "All crawlers from TASK-038 registered in `CRAWLER_REGISTRY`"
  - "Rate limiter prevents exceeding configured req/sec (verified with timing test)"
  - "Manual trigger via admin API queues the task immediately"
  - "Paused crawler skips scheduled runs without error"
  - "Health alert created after 3 consecutive failures (tested with mock failures)"
  - "Crawl run history accessible via admin API"
  - "Rate limit state stored in Redis (survives worker restart)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-009 Platform Integrations
mhs_agent: Data Crawler
mhs_model: gemini-2.5-pro
mhs_estimated_tokens: 25000
mhs_estimated_hours: 3
---

# TASK-039 — Crawl Scheduler + Rate Limiter

## Description

Make all crawlers permanent and manageable: a unified scheduler UI in the
admin dashboard, per-crawler rate limiting, and a health monitor that alerts
when a crawler fails repeatedly.

## Scheduler configuration

Each crawler declares its schedule in `crawlers/registry.py`:

```python
CRAWLER_REGISTRY = {
    "idealist":     CrawlerConfig(schedule=crontab(hour=2),          rate=2),
    "un_volunteers":CrawlerConfig(schedule=crontab(day_of_week=1),   rate=2),
    "nobel":        CrawlerConfig(schedule=crontab(month_of_year=10),rate=5),
    "github_sync":  CrawlerConfig(schedule=crontab(hour="*/6"),      rate=10),
    "linkedin_sync":CrawlerConfig(schedule=crontab(hour=3),          rate=5),
    "carbon_update":CrawlerConfig(schedule=crontab(day_of_week=1, hour=2), rate=10),
}
```

## Rate limiter middleware

Using `limits` library — enforced per crawler, not globally:

```python
from limits import storage, strategies, parse

class RateLimitedCrawler(BaseCrawler):
    def __init__(self, crawler_name: str, rate_per_second: int):
        self._limiter = strategies.MovingWindowRateLimiter(
            storage.RedisStorage(REDIS_URL)
        )
        self._rate = parse(f"{rate_per_second}/second")
        self._key = f"crawler:{crawler_name}"

    async def fetch(self, url: str) -> dict:
        if not self._limiter.hit(self._rate, self._key):
            await asyncio.sleep(1.0 / self._rate_per_second)
        return await super().fetch(url)
```

## Admin API endpoints (add to TASK-027 scope)

```
GET  /admin/crawlers                    # List all crawlers + status
POST /admin/crawlers/{name}/trigger     # Manual trigger
POST /admin/crawlers/{name}/pause       # Pause a crawler
POST /admin/crawlers/{name}/resume      # Resume
GET  /admin/crawlers/{name}/history     # Last 20 run results
```

## Health monitoring

- If a crawler fails 3 consecutive runs → send alert to `admin_notifications` table
- Admin dashboard shows crawler health: green (last run OK) / yellow (1-2 failures) / red (3+)
- Crawl run log stored in `crawl_runs` table (crawler_name, started_at, finished_at, status, items, error)

## Acceptance Criteria

- [ ] All crawlers from TASK-038 registered in `CRAWLER_REGISTRY`
- [ ] Rate limiter prevents exceeding configured req/sec (verified with timing test)
- [ ] Manual trigger via admin API queues the task immediately
- [ ] Paused crawler skips scheduled runs without error
- [ ] Health alert created after 3 consecutive failures (tested with mock failures)
- [ ] Crawl run history accessible via admin API
- [ ] Rate limit state stored in Redis (survives worker restart)
