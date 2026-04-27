---
id: TASK-40
assignee: []
title: "Public Statistics Dashboard"
status: To Do
priority: medium
labels: ["epic012-frontend-ui/ux", "sonnet", "data-visualizer"]
dependencies:
  - task-5
  - task-8
  - task-9
acceptance_criteria:
  - "`/stats` page loads without authentication"
  - "All 6 chart components render without errors"
  - "Countries with < 5 activities show as suppressed on map"
  - "API endpoints cached in Redis (verify: second request faster than first)"
  - "Page passes axe-core accessibility check (0 violations)"
  - "No individual user data anywhere in page or API responses"
  - "Mobile layout stacks charts vertically (tested at 375px)"
  - "`npm run build` passes TypeScript checks"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-012 Frontend UI/UX
mhs_agent: Data Visualizer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-040 — Public Statistics Dashboard

## Description

A public `/stats` page showing anonymized, aggregated platform statistics.
No individual user data. No authentication required. Beautiful and informative.

## Page layout

```
/stats
├── Hero: "My Humanity Score (MHS) by the numbers" + last-updated timestamp
├── Row 1 (4 metric cards):
│   ├── Total verified activities
│   ├── Total users
│   ├── Countries represented
│   └── Average MHS score globally
├── Row 2:
│   ├── [Wide] Activity by category (horizontal bar chart)
│   └── [Narrow] Score level distribution (donut chart)
├── Row 3:
│   └── [Full width] Geographic impact map (choropleth — activities by country)
├── Row 4:
│   ├── Platform growth over time (line chart: users + activities by month)
│   └── Top activity types this week (horizontal bar)
└── Footer: "All data anonymized and aggregated. Min group size: 5."
```

## New API endpoints needed (add to `routers/stats.py`)

```
GET /stats/overview
  → { total_activities, total_users, countries_count, avg_score }

GET /stats/activities/by-category
  → [{ category, count, pct }]

GET /stats/scores/distribution
  → [{ level, count, pct }]  -- 7 score levels

GET /stats/geographic
  → [{ country_code, country_name, activity_count }]
  -- suppress countries with count < 5 (anonymization)

GET /stats/growth?months=12
  → [{ month, user_count, activity_count }]

GET /stats/activities/trending?days=7
  → [{ activity_type, count }] top 10
```

All endpoints: cache in Redis (TTL 15 min), no auth required.

## Chart components to build

| Component | Library | File |
|---|---|---|
| `MetricCard` | — (plain div) | `components/stats/MetricCard.tsx` |
| `ActivityByCategoryBar` | recharts HorizontalBar | `components/stats/ActivityByCategoryBar.tsx` |
| `ScoreLevelDonut` | recharts PieChart | `components/stats/ScoreLevelDonut.tsx` |
| `GeographicMap` | react-simple-maps | `components/stats/GeographicMap.tsx` |
| `GrowthLineChart` | recharts LineChart | `components/stats/GrowthLineChart.tsx` |
| `TrendingActivities` | recharts HorizontalBar | `components/stats/TrendingActivities.tsx` |

## Design requirements

- Use `CATEGORY_COLORS` from `.vibe/agents/data-visualizer.md` for bar colors
- Score level donut uses level colors (🌱 green → 👑 gold gradient)
- Geographic map: Angel gold fill, intensity by activity count
- All charts dark mode (background `#0F172A`)
- Mobile: stack all charts vertically (single column)

## Anonymization enforcement

```typescript
// Applied in API layer before response:
function suppressSmallGroups(data: GeoEntry[], minSize = 5): GeoEntry[] {
  return data.map(d => d.activity_count < minSize
    ? { ...d, activity_count: null, suppressed: true }
    : d
  )
}
```

## Acceptance Criteria

- [ ] `/stats` page loads without authentication
- [ ] All 6 chart components render without errors
- [ ] Countries with < 5 activities show as suppressed on map
- [ ] API endpoints cached in Redis (verify: second request faster than first)
- [ ] Page passes axe-core accessibility check (0 violations)
- [ ] No individual user data anywhere in page or API responses
- [ ] Mobile layout stacks charts vertically (tested at 375px)
- [ ] `npm run build` passes TypeScript checks
