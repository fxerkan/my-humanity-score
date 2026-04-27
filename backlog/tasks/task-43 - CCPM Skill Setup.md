---
id: TASK-43
assignee: []
title: "CCPM Skill Setup"
status: Done
priority: high
labels: ["epic001-foundation-&-infrastructure", "haiku", "developer"]
dependencies: []
acceptance_criteria:
  - "CCPM repo cloned from https://github.com/automazeio/ccpm"
  - "ccpm skill symlinked to ~/.claude/skills/ccpm"
  - "SKILL.md readable by Claude Code"
  - "gh CLI authenticated (prerequisite for CCPM GitHub operations)"
created_date: '2026-04-27 13:45'
updated_date: '2026-04-27 13:45'
mhs_epic: EPIC-001 Foundation & Infrastructure
mhs_agent: Developer
mhs_model: claude-haiku-4-5
mhs_estimated_tokens: 3000
mhs_estimated_hours: 0
---

# TASK-043 — CCPM Skill Setup

## Description
Install the CCPM (https://github.com/automazeio/ccpm) agent skill for spec-driven project
management. CCPM is NOT a CLI — it is an agent skill that extends Claude Code with PRD →
Epic → GitHub Issues → Parallel Agents workflow.

## Installation
```bash
git clone https://github.com/automazeio/ccpm.git /tmp/ccpm
ln -sf /tmp/ccpm/skill/ccpm ~/.claude/skills/ccpm
```

## Usage
CCPM is activated via natural language in Claude Code:
- "Write a PRD for [feature]"
- "Parse this PRD into an epic"
- "Decompose the epic into tasks"
- "Sync to GitHub"
- "Start working on issue N"
- "Run the standup"

## Prerequisites
- `gh` CLI must be authenticated (`gh auth login`)
- Git repo with remote GitHub origin
