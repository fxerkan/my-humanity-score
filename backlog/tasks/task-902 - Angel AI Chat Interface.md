---
id: TASK-902
assignee: []
title: "Angel AI Chat Interface"
status: To Do
priority: medium
labels: ["epic005-angel-ai-system", "sonnet", "developer", "post-mvp"]
dependencies:
  - task-5
  - task-900
acceptance_criteria:
  - "Monthly summary renders formatted report correctly"
  - "Chat sends message and streams response token by token"
  - "Guardian warnings display with correct color coding"
  - "Empty state for new users: \"Welcome! I'm Angel, your mentor.\""
  - "Chat input disabled during streaming response"
  - "Keyboard accessible (Enter to send, Escape to clear)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-005 Angel AI System
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 30000
mhs_estimated_hours: 3
---

> **⏳ POST-MVP:** Bu modül MVP tamamlandıktan sonra geliştirilecek.

# TASK-033 — Angel AI Chat Interface

## Description
Chat-style UI for interacting with Angel AI. Displays both Guardian
warnings and Mentor messages in a unified interface.

## UI layout
```
/angel
┌─────────────────────────────────────┐
│  👼 Angel AI                        │
│  Your guardian and mentor           │
├─────────────────────────────────────┤
│  [Monthly Summary]  [Ask Angel]     │  ← tabs
├─────────────────────────────────────┤
│  Monthly Summary tab:               │
│  ┌──────────────────────────────┐   │
│  │ April Impact Report          │   │
│  │ Score: 342 (+18) 💫          │   │
│  │ Top: Social Impact           │   │
│  │ New badge: 🩸 Blood Donor    │   │
│  └──────────────────────────────┘   │
│                                     │
│  Suggested next steps:              │
│  • 🌱 Plant a tree (+5 pts)         │
│  • 📖 Mentor someone (+4 pts)       │
│                                     │
│  Ask Angel tab:                     │
│  [User message input]               │
│  [Angel's response bubble]          │
└─────────────────────────────────────┘
```

## Guardian notifications
- Appear as inline warning cards in the chat
- Yellow border for LOW/MEDIUM, red for HIGH/CRITICAL
- Include action taken + appeal link

## Chat functionality
- Chat history persisted per session (not across sessions)
- Streaming response (SSE from `/mentor/chat` endpoint)
- Angel cannot be used to discriminate (blocked prompts return gentle redirect)

## API endpoints needed (add to TASK-016 scope)
```
GET  /mentor/monthly-summary    # Monthly summary data
POST /mentor/chat               # Send message to Angel (SSE response)
```

## Acceptance Criteria
- [ ] Monthly summary renders formatted report correctly
- [ ] Chat sends message and streams response token by token
- [ ] Guardian warnings display with correct color coding
- [ ] Empty state for new users: "Welcome! I'm Angel, your mentor."
- [ ] Chat input disabled during streaming response
- [ ] Keyboard accessible (Enter to send, Escape to clear)
