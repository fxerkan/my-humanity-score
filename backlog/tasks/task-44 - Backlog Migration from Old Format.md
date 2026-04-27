---
id: TASK-44
assignee: []
title: "Backlog Migration from Old Format"
status: Done
priority: high
labels: ["epic001-foundation-&-infrastructure", "haiku", "developer"]
dependencies:
  - task-42
acceptance_criteria:
  - "All 41 original task files migrated to Backlog.md format"
  - "All tasks visible in backlog task list --plain"
  - "Old backlog/tasks/, backlog/epics/, backlog/sprints/ directories removed"
  - "Epics moved to backlog/docs/epics/"
  - "Sprints moved to backlog/docs/sprints/"
  - "All task frontmatters include: id, title, status, priority, labels, created_date"
created_date: '2026-04-27 13:45'
updated_date: '2026-04-27 13:45'
mhs_epic: EPIC-001 Foundation & Infrastructure
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 5000
mhs_estimated_hours: 1
---

# TASK-044 — Backlog Migration from Old Format

## Description
Migrate the existing backlog from MHS-custom format to Backlog.md-compatible format.

## Migration scripts
- `scripts/migrate-backlog.py` — main migration (old format → Backlog.md frontmatter)
- `scripts/fix-backlog-frontmatter.py` — post-migration fix (adds id, created_date, fixes YAML)

## What was migrated
- 41 tasks from `backlog/tasks/task-NNN-slug.md` → `backlog/tasks/task-N - Title.md`
- 12 epics from `backlog/epics/` → `backlog/docs/epics/`
- 1 sprint file from `backlog/sprints/` → `backlog/docs/sprints/`

## Directory structure after migration
```
backlog/
  tasks/           ← 41 task files (Backlog.md format)
  docs/
    epics/         ← 12 epic docs
    sprints/       ← Sprint planning docs
  config.yml       ← Backlog.md project config
  archive/         ← Created by backlog init
  completed/       ← For completed tasks
```
