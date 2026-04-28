---
id: TASK-42
assignee: []
title: "Backlog.md Installation and Configuration"
status: Done
priority: high
labels: ["epic001-foundation-&-infrastructure", "haiku", "developer"]
dependencies: []
acceptance_criteria:
  - "backlog CLI installed globally (npm i -g backlog.md)"
  - "backlog task list shows all 41 tasks"
  - "backlog browser starts on port 6420"
  - "backlog MCP server registered in Claude Code user config"
  - "backlog/config.yml created with project settings"
  - "All task files use Backlog.md-compatible frontmatter (id, status, priority, created_date)"
created_date: '2026-04-27 13:45'
updated_date: '2026-04-27 13:45'
mhs_epic: EPIC-001 Foundation & Infrastructure
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 5000
mhs_estimated_hours: 1
---

# TASK-042 — Backlog.md Installation and Configuration

## Description
Install and configure Backlog.md (https://github.com/MrLesk/Backlog.md) for task management.
Migrate all existing task files from the old flat format to Backlog.md-compatible frontmatter.
Set up the backlog browser for visual task management.

## What was done
- Installed backlog.md v1.44.0 globally via npm
- Ran migration script (`scripts/migrate-backlog.py`) to convert 41 tasks
- Ran fix script (`scripts/fix-backlog-frontmatter.py`) to add required `id`, `created_date` fields
- Fixed YAML escaping issues in acceptance_criteria (embedded double quotes)
- Moved task files to `backlog/tasks/` (Backlog.md v1.44 expects this location)
- Configured `backlog/config.yml`
- Registered Backlog.md MCP server: `claude mcp add backlog --scope user -- backlog mcp start`
- backlog browser running at http://localhost:6420
