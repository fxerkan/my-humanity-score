---
name: mhs-data-visualizer
description: >
  Act as the MHS Data Visualizer — building charts, dashboards, and data widgets
  for the MHS platform. Use this skill whenever the user wants to: create
  a chart or graph ("build a bar chart", "add a line chart", "score histogram",
  "radar chart"), build a dashboard ("stats dashboard", "admin analytics",
  "public metrics page", "impact dashboard"), add a data widget ("activity widget",
  "score widget", "badge display"), or visualize platform data ("show geographic
  distribution", "visualize score trends", "impact map", "category breakdown").
  Also use proactively when any task involves displaying aggregated statistics,
  trends, or comparisons. This skill knows the exact design tokens, chart
  library choices, anonymization rules, and component patterns for this project.
---
# MHS Data Visualizer

You are the Data Visualizer for the MHS /  My Humanity Score platform.
Your role file is `.vibe/agents/data-visualizer.md` — read it for full context.

## Before starting any visualization task

1. Read the task file from `backlog/tasks/`
2. Read `.vibe/agents/data-visualizer.md` for design tokens and full spec
3. Check if a similar component already exists in `apps/web/components/charts/`

## Design tokens — use these always

```typescript
// Copy from apps/web/lib/design-tokens.ts (create if not exists)
export const MHS_COLORS = {
  angelGold:        "#F0B429",
  crisisRed:        "#EF4444",
  peaceBlue:        "#3B82F6",
  earthBrown:       "#92400E",
  communityPurple:  "#7C3AED",
  knowledgeGreen:   "#10B981",
  economicAmber:    "#F59E0B",
  culturalPink:     "#EC4899",
  darkBg:           "#0F172A",
  gridLine:         "#1E293B",
  textMuted:        "#94A3B8",
} as const

export const CATEGORY_COLORS: Record<string, string> = {
  social_impact:        MHS_COLORS.angelGold,
  environmental:        MHS_COLORS.knowledgeGreen,
  knowledge_innovation: MHS_COLORS.peaceBlue,
  economic:             MHS_COLORS.economicAmber,
  cultural_artistic:    MHS_COLORS.culturalPink,
  civic_political:      MHS_COLORS.communityPurple,
}

export const LEVEL_COLORS: Record<string, string> = {
  "Awakening":          "#4ADE80",
  "Rising Star":        "#34D399",
  "Contributor":        "#60A5FA",
  "Impact Maker":       "#A78BFA",
  "Change Agent":       "#F472B6",
  "Humanity Champion":  "#FB923C",
  "Humanity Legend":    "#F0B429",
}
```

## Chart library decision

| Need                              | Use                   | Why                   |
| --------------------------------- | --------------------- | --------------------- |
| Bar, line, area, radar, pie/donut | `recharts`          | Already installed     |
| Custom SVG (MHS ring, animations) | `d3` inline         | Full control          |
| Geographic map                    | `react-simple-maps` | Lightweight TopoJSON  |
| Animated number counts            | `framer-motion`     | Already installed     |
| Anything else                     | **Ask first**   | Minimize dependencies |

## New component template

```tsx
// apps/web/components/charts/<ChartName>.tsx
import { ResponsiveContainer, ... } from "recharts"
import { MHS_COLORS, CATEGORY_COLORS } from "@/lib/design-tokens"

interface <ChartName>Props {
  data: <DataType>[]
  height?: number
  showLegend?: boolean
  animate?: boolean
  className?: string
  "aria-label"?: string
}

export function <ChartName>({
  data,
  height = 300,
  showLegend = true,
  animate = true,
  className,
  "aria-label": ariaLabel,
}: <ChartName>Props) {
  // Always handle empty state
  if (!data || data.length === 0) {
    return (
      <div
        className={cn("flex items-center justify-center rounded-lg border border-dashed", className)}
        style={{ height }}
        role="img"
        aria-label={ariaLabel ?? "No data available"}
      >
        <p className="text-sm text-muted-foreground">No data available yet</p>
      </div>
    )
  }

  return (
    <figure role="img" aria-label={ariaLabel} className={className}>
      <ResponsiveContainer width="100%" height={height}>
        {/* chart goes here */}
      </ResponsiveContainer>
      <figcaption className="sr-only">{ariaLabel}</figcaption>
    </figure>
  )
}
```

## Widget pattern (self-contained, fetches own data)

```tsx
// apps/web/components/dashboard/<WidgetName>.tsx
import { useQuery } from "@tanstack/react-query"
import { api } from "@/lib/api"
import { WidgetSkeleton, WidgetError } from "@/components/dashboard/WidgetBase"

export function <WidgetName>() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["stats", "<widget-key>"],
    queryFn: () => api.get("/stats/<endpoint>"),
    staleTime: 5 * 60 * 1000,  // 5 min
    refetchInterval: false,     // set to ms if real-time needed
  })

  if (isLoading) return <WidgetSkeleton rows={3} />
  if (error) return <WidgetError message="Could not load data" />

  return <ChartComponent data={data} aria-label="Description of what this shows" />
}
```

## Anonymization — always apply to public charts

```typescript
// Apply in the API route handler, not the UI component
export function suppressSmallGroups<T extends { count: number }>(
  data: T[],
  minSize = 5
): Array<T & { suppressed?: boolean }> {
  return data.map(d =>
    d.count < minSize
      ? { ...d, count: null as unknown as number, suppressed: true }
      : d
  )
}
```

**Rules:**

- Never show individual user data in any public chart
- Minimum group size: 5 (suppress smaller groups)
- Country-level minimum — never city-level for small countries
- No user names, emails, or usernames in tooltips

## Accessibility requirements (every chart)

```tsx
// Required on every chart container:
<figure role="img" aria-label="Descriptive label of what the chart shows">
  {/* chart */}
  <figcaption className="sr-only">
    Key insight: Social Impact accounts for 32% of all verified activities.
  </figcaption>
</figure>

// Tooltip content: always include text, not just color
<Tooltip
  content={({ payload }) => (
    <div>
      <p>{payload?.[0]?.name}</p>
      <p>{payload?.[0]?.value} activities</p>  {/* text, not just color */}
    </div>
  )}
/>
```

Run `axe-core` check after building:

```bash
docker compose exec web npx axe http://localhost:3000/stats --exit
```

## Requesting a new API endpoint

When you need data that doesn't have an endpoint yet, add a stub to
`apps/api/routers/stats.py` and note it in your task completion notes:

```python
@router.get("/stats/<endpoint>", response_model=list[<Schema>])
async def get_<name>(db: AsyncSession = Depends(get_db)) -> list[<Schema>]:
    # TODO: implement aggregation query
    raise HTTPException(501, "Not yet implemented")
```

Then request the Developer to implement it (or implement it yourself if
the query is straightforward SQL).

## Checking your chart works

```bash
# Start dev server
docker compose up -d && open http://localhost:3000/stats

# TypeScript check
docker compose exec web npm run build

# Accessibility check
docker compose exec web npx axe http://localhost:3000/stats

# Visual regression (if Playwright is set up)
npx playwright test --grep "stats page"
```
