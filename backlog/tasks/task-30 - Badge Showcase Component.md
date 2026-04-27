---
id: TASK-30
assignee: []
title: "Badge Showcase Component"
status: To Do
priority: high
labels: ["epic006-badge-&-achievement-system", "haiku", "developer"]
dependencies:
  - task-5
acceptance_criteria:
  - "Earned badges render in full color with correct emoji"
  - "Locked badges show in grayscale with lock overlay"
  - "Hover tooltip shows criteria and earned date"
  - "Empty state renders when no badges earned"
  - "Layer 3 honorary titles have distinct visual treatment (glow/border)"
  - "Accessible: all badges have aria-label with name + status"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-006 Badge & Achievement System
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 15000
mhs_estimated_hours: 2
---

# TASK-030 — Badge Showcase Component

## Description
Badge grid component for the profile page displaying all 4 badge layers
with earned/locked states and hover tooltips.

## Badge data structure
```typescript
interface Badge {
  id: string
  type: string
  layer: 1 | 2 | 3 | 4
  emoji: string
  name: string
  description: string
  criteria: string
  earnedAt?: string  // ISO date or undefined (locked)
  rarity?: "common" | "rare" | "legendary"
}
```

## Component sections
1. **Level badge** (Layer 1) — large, current level displayed prominently
2. **Activity badges** (Layer 2) — 17 badges in 3-column grid
3. **Honorary titles** (Layer 3) — special display with glow effect
4. **Group badges** (Layer 4) — shown if group member earned them

## States
- **Earned**: full color + emoji, showing earned date on hover
- **Locked**: grayscale + lock icon, showing criteria on hover
- **Empty state**: "Start your journey →" CTA pointing to /claim

## Tooltip content on hover
```
🩸 Blood Donor
Earned: April 15, 2026
"Donated blood at least once"
```

## Component location
`apps/web/components/badges/BadgeShowcase.tsx`
`apps/web/components/badges/BadgeItem.tsx`

## Acceptance Criteria
- [ ] Earned badges render in full color with correct emoji
- [ ] Locked badges show in grayscale with lock overlay
- [ ] Hover tooltip shows criteria and earned date
- [ ] Empty state renders when no badges earned
- [ ] Layer 3 honorary titles have distinct visual treatment (glow/border)
- [ ] Accessible: all badges have aria-label with name + status
