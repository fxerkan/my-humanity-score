---
id: TASK-38
assignee: []
title: "NGO & Registry Web Crawlers"
status: To Do
priority: medium
labels: ["epic004-activity-system-&-verification", "gemini-pro", "data-crawler"]
dependencies:
  - task-3
  - task-20
acceptance_criteria:
  - "All crawlers respect rate limits (verified with mock HTTP and timing assertions)"
  - "`User-Agent` header set on every request"
  - "`robots.txt` checked before crawling any domain"
  - "Crawl state persists across restarts (resume test: interrupt mid-crawl, restart)"
  - "Nobel crawler correctly populates Nobel 2024 laureates in test DB"
  - "ORCID on-demand lookup returns works for a known test ORCID ID"
  - "Unit tests mock all HTTP calls (no live API calls in CI)"
  - "Integration test documented with setup instructions for live API keys"
  - "`ngo_registry` deduplicates on `(source, external_id)`"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-004 Activity System & Verification
mhs_agent: Data Crawler
mhs_model: gemini-2.5-pro
mhs_estimated_tokens: 40000
mhs_estimated_hours: 5
---

# TASK-038 — NGO & Registry Web Crawlers

## Description

Build async crawlers for the 4 most important NGO and public registry APIs
used in the activity verification pipeline (Layer 1). Each crawler is a
Celery task that runs on a schedule and stores results in a local lookup table.

## Crawlers to build

### 1. Idealist volunteer registry (`crawlers/idealist.py`)
- API: `https://api.idealist.org/v1/actions?type=volunteering`
- Auth: API key via `IDEALIST_API_KEY` env var
- Data: org name, location, volunteer opportunity ID, dates
- Schedule: daily sync of new opportunities
- Lookup table: `ngo_registry` (org_name, source, external_id, verified_at)

### 2. UN Volunteers public feed (`crawlers/un_volunteers.py`)
- API: `https://api.unv.org/opportunities` (public, no auth)
- Data: assignment title, org, country, category
- Schedule: weekly full sync
- Rate limit: 2 req/sec max

### 3. Nobel Prize laureates (`crawlers/nobel.py`)
- API: `https://api.nobelprize.org/2.1/laureates`
- Public, no auth required
- Data: name, year, category, motivation text
- Schedule: annual (Nobel announced in October)
- This populates auto-verification for Nobel claims

### 4. ORCID public profiles (`crawlers/orcid.py`)
- API: `https://pub.orcid.org/v3.0/` (public read)
- On-demand only (triggered when user submits academic claim with ORCID ID)
- Data: works, employments, funding, education
- No bulk crawl — per-request lookup only

## Shared infrastructure

### Base crawler class (`crawlers/base.py`)
```python
class BaseCrawler:
    rate_limit: int = 1        # requests per second
    retry_attempts: int = 3
    timeout: float = 10.0
    user_agent = "My Humanity Score (MHS)-Bot/1.0 (+https://My Humanity Score (MHS).app/bot)"

    async def fetch(self, url: str) -> dict: ...
    def save_crawl_state(self, cursor: str, count: int) -> None: ...
    def load_crawl_state(self) -> CrawlState | None: ...
```

### Crawl state table (add to Alembic migration)
```sql
CREATE TABLE crawl_states (
  crawler_name VARCHAR(50) PRIMARY KEY,
  last_cursor TEXT,
  items_processed INTEGER DEFAULT 0,
  last_run_at TIMESTAMPTZ,
  status VARCHAR(20) DEFAULT 'idle'
);
```

### NGO registry lookup table
```sql
CREATE TABLE ngo_registry (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_name VARCHAR(255),
  org_name_normalized VARCHAR(255),  -- lowercase, stripped
  source VARCHAR(50),                 -- 'idealist'|'unv'|'nobel'|'orcid'
  external_id VARCHAR(255),
  metadata JSONB,
  crawled_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(source, external_id)
);
```

## Acceptance Criteria

- [ ] All crawlers respect rate limits (verified with mock HTTP and timing assertions)
- [ ] `User-Agent` header set on every request
- [ ] `robots.txt` checked before crawling any domain
- [ ] Crawl state persists across restarts (resume test: interrupt mid-crawl, restart)
- [ ] Nobel crawler correctly populates Nobel 2024 laureates in test DB
- [ ] ORCID on-demand lookup returns works for a known test ORCID ID
- [ ] Unit tests mock all HTTP calls (no live API calls in CI)
- [ ] Integration test documented with setup instructions for live API keys
- [ ] `ngo_registry` deduplicates on `(source, external_id)`
