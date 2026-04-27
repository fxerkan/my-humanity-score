---
id: TASK-41
assignee: []
title: "Admin Analytics Widgets"
status: To Do
priority: low
labels: ["epic010-admin-&-governance", "sonnet", "data-visualizer"]
dependencies:
  - task-5
  - task-27
  - task-40
acceptance_criteria:
  - "All 6 widget components render with seed data"
  - "Non-admin JWT returns 403 on all `/admin/analytics/*` routes"
  - "Queue depths widget auto-refreshes every 30 seconds"
  - "Bias parity chart shows red zone correctly at ±15% threshold"
  - "Guardian timeline drill-down opens event list modal"
  - "Widgets show loading skeleton (not blank) while fetching"
  - "All charts pass axe-core check"
  - "Admin dashboard layout uses CSS grid (responsive, 2 cols on desktop)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-010 Admin & Governance
mhs_agent: Data Visualizer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 30000
mhs_estimated_hours: 3
---

# TASK-041 — Admin Analytics Widgets

## Description

Analytics widgets for the admin dashboard (`/admin/analytics`).
These show operational metrics visible only to admins: pipeline health,
Angel AI activity, verification queue depth, and bias audit results.

## Dashboard sections

### 1. Verification Pipeline Funnel
Shows how many activities pass through each verification layer.

```
Submitted → Auto API check → OCR/AI → Peer Review → Org Email → Ethics Board → Verified
  1,240       980 (79%)      820      420            180          12            1,100
```

Component: `VerificationFunnel.tsx` using recharts `FunnelChart`.

### 2. Daily Active Users (30-day line chart)
- Metric: unique users who logged in or submitted an activity
- Component: `DAUChart.tsx` using recharts `LineChart`
- Includes: 7-day moving average line

### 3. Score Distribution Histogram (animated)
- Bins: 0–99, 100–249, 250–399, 400–549, 550–699, 700–849, 850–1000
- Updates weekly (not real-time)
- Color-coded by level (🌱 green → 👑 gold)
- Component: `ScoreHistogram.tsx`

### 4. Pending Queue Depths (live, 30-sec refresh)
- Bar chart: queue depth per verification layer
- Red threshold line at 50 (alert level)
- Component: `QueueDepths.tsx`

### 5. Angel AI Event Timeline (last 7 days)
- Stacked area chart: events by threat level (LOW/MEDIUM/HIGH/CRITICAL)
- Drill-down: click a spike → list of events in that time window
- Component: `GuardianTimeline.tsx`

### 6. Bias Audit Parity Chart
- Grouped horizontal bar: mean MHS score by gender groups / age groups / regions
- Reference line at global mean
- Red zone: ±15% from global mean (auto-flagged)
- Component: `BiasParityChart.tsx`

## New admin API endpoints (add to `routers/admin.py`)

```
GET /admin/analytics/funnel           # Verification funnel counts
GET /admin/analytics/dau?days=30      # Daily active users
GET /admin/analytics/score-histogram  # Score distribution
GET /admin/analytics/queue-depths     # Live queue sizes
GET /admin/analytics/guardian-events?days=7  # Threat event counts by level
GET /admin/analytics/bias-parity      # Latest bias audit parity data
```

All require `role=admin` JWT claim.

## Acceptance Criteria

- [ ] All 6 widget components render with seed data
- [ ] Non-admin JWT returns 403 on all `/admin/analytics/*` routes
- [ ] Queue depths widget auto-refreshes every 30 seconds
- [ ] Bias parity chart shows red zone correctly at ±15% threshold
- [ ] Guardian timeline drill-down opens event list modal
- [ ] Widgets show loading skeleton (not blank) while fetching
- [ ] All charts pass axe-core check
- [ ] Admin dashboard layout uses CSS grid (responsive, 2 cols on desktop)
