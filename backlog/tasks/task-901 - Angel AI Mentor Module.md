---
id: TASK-901
assignee: []
title: "Angel AI Mentor Module"
status: To Do
priority: medium
labels: ["epic005-angel-ai-system", "sonnet", "developer", "post-mvp"]
dependencies:
  - task-7
  - task-900
acceptance_criteria:
  - "Monthly summary generated for all active users on 1st of month"
  - "Summary includes score delta, top category, new badges, suggestions"
  - "Suggestions are relevant to user's activity history (not generic)"
  - "No mention of forbidden features (religion, nationality, etc.) in any prompt"
  - "LLM output passes through Guardian toxicity check before delivery"
  - "Summary stored and retrievable (not regenerated on every GET)"
  - "Celery schedule job logs success/failure per user"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-005 Angel AI System
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 40000
mhs_estimated_hours: 4
---

> **⏳ POST-MVP:** Bu modül MVP tamamlandıktan sonra geliştirilecek.

# TASK-016 — Angel AI Mentor Module

## Description
The Mentor module: generates personalized monthly impact summaries,
next-action suggestions, and motivation nudges for each user.
Uses an open-source LLM (Llama 3.3-70b or Mistral) via Ollama.

## Monthly impact summary
Generated on the 1st of each month via Celery scheduled task.
```
📊 Your April Impact Report

Your MHS score: 342 (+18 this month) 💫

Top category: Social Impact (+12)
New badges: 🩸 Blood Donor

Your highlights:
• Donated blood on April 15 (+8 pts)
• Completed online Python course (+6 pts)

Suggested next steps:
1. 🌱 Plant a tree this month (Environmental: +5 pts estimated)
2. 📖 Mentor someone in your area of expertise (+4 pts)

You're in the top 22% globally — keep going!
```

## Next-action suggestions
- Based on: current category scores, past activities, local events
- Suggestions ranked by: estimated impact × feasibility × time required
- Filter by user's stated interests from onboarding questionnaire

## Motivation nudge notifications
- Triggers: score milestone approaching, similar user achieved next level,
  badge criteria nearly met, 30 days without activity
- Tone: warm, non-pressuring, culturally neutral
- Language: adapts to user's preferred language

## LLM integration
- Model: `llama3.3:70b` via Ollama (self-hosted) or Claude API fallback
- System prompt: loads from `.vibe/agents/angel-mentor-system-prompt.md`
- Temperature: 0.7 (creative but coherent)
- Max tokens: 500 per summary

## API
```
GET /mentor/monthly-summary         # Generate/retrieve current month summary
GET /mentor/suggestions             # Personalized next-action list
POST /mentor/nudge                  # Trigger immediate nudge (admin/test)
```

## Acceptance Criteria
- [ ] Monthly summary generated for all active users on 1st of month
- [ ] Summary includes score delta, top category, new badges, suggestions
- [ ] Suggestions are relevant to user's activity history (not generic)
- [ ] No mention of forbidden features (religion, nationality, etc.) in any prompt
- [ ] LLM output passes through Guardian toxicity check before delivery
- [ ] Summary stored and retrievable (not regenerated on every GET)
- [ ] Celery schedule job logs success/failure per user
