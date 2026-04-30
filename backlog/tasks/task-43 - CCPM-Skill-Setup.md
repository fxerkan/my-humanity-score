---
id: TASK-43
title: CCPM Skill Setup
status: Done
assignee: []
created_date: '2026-04-27 13:45'
updated_date: '2026-04-30 07:10'
labels:
  - epic001-foundation-&-infrastructure
  - haiku
  - developer
dependencies: []
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
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
<!-- SECTION:DESCRIPTION:END -->

# TASK-043 — CCPM Skill Setup
