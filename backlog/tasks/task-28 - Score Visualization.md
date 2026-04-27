---
id: TASK-28
assignee: []
title: "Score Visualization"
status: To Do
priority: high
labels: ["epic012-frontend-ui/ux", "sonnet", "developer"]
dependencies:
  - task-5
  - task-8
acceptance_criteria:
  - "Ring animation plays on initial page load"
  - "Radar chart renders all 6 axes with correct labels"
  - "Both components work with score = 0 (empty/dashed state)"
  - "No layout shift on load (fixed dimensions)"
  - "Accessible: ARIA labels on SVG, color not sole differentiator"
  - "Storybook stories for: empty state, 50% filled, fully maxed"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-012 Frontend UI/UX
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 20000
mhs_estimated_hours: 2
---

# TASK-028 — Score Visualization (Radar Chart)

## Description
Score visualization components for the profile page:
a circular MHS ring + a radar (spider) chart for the 6 categories.

## MHS Ring component
- SVG circle with progress fill (0–1000 range)
- Center: large score number + level emoji
- Color: Angel gold (#F0B429) for filled arc
- Animated on mount (0 → score in 1.5s)

## Radar chart component
- Library: `recharts` RadarChart or `chart.js` with React wrapper
- 6 axes: Social Impact, Environmental, Knowledge, Economic, Cultural, Civic
- Filled polygon with MHS category colors
- Hover tooltip: category name + score + weight
- Empty state: dashed outline radar (for new users)

## Component API
```tsx
<MHSRing score={342} level="Contributor" animated />
<CategoryRadar
  scores={{
    social_impact: 180,
    environmental: 120,
    knowledge_innovation: 200,
    economic: 100,
    cultural_artistic: 80,
    civic_political: 100,
  }}
/>
```

## File locations
- `apps/web/components/score/MHSRing.tsx`
- `apps/web/components/score/CategoryRadar.tsx`

## Acceptance Criteria
- [ ] Ring animation plays on initial page load
- [ ] Radar chart renders all 6 axes with correct labels
- [ ] Both components work with score = 0 (empty/dashed state)
- [ ] No layout shift on load (fixed dimensions)
- [ ] Accessible: ARIA labels on SVG, color not sole differentiator
- [ ] Storybook stories for: empty state, 50% filled, fully maxed
