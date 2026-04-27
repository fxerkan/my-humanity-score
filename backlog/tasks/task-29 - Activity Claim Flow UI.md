---
id: TASK-29
assignee: []
title: "Activity Claim Flow UI"
status: To Do
priority: high
labels: ["epic012-frontend-ui/ux", "sonnet", "developer"]
dependencies:
  - task-5
  - task-10
acceptance_criteria:
  - "Step progress saved in state (going back doesn't lose data)"
  - "File upload shows preview and size validation error"
  - "Angel AI pre-review step shows spinner while checking"
  - "Form cannot submit with required fields empty"
  - "Successful submission shows confirmation with activity ID"
  - "Mobile-friendly stepper (horizontal on desktop, vertical on mobile)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-012 Frontend UI/UX
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 35000
mhs_estimated_hours: 4
---

# TASK-029 — Activity Claim Flow UI (5-Step Wizard)

## Description
5-step activity claim wizard. Users submit activities with evidence;
Angel AI pre-review runs before community verification.

## Step 1 — Activity Type
- Grid of 5 category cards: Humanitarian, Science & Innovation,
  Community, Environment, Education
- Each with icon, description, example activities

## Step 2 — Activity Details
- Title (required)
- Description (optional, 500 char max)
- Activity date (date picker)
- Subcategory select (populated by selected type)

## Step 3 — Evidence
- Evidence URL input (with validation)
- OR file upload (PDF/JPG/PNG, max 10MB)
- OR "No evidence — request peer review directly"
- Preview for uploaded files

## Step 4 — Angel AI Pre-Review
- Loading state: "Angel is reviewing your submission..."
- Result: ✅ Looks good! OR ⚠️ Potential issue: [message]
- User can still submit despite warning
- Guardian check runs in background (TASK-015)

## Step 5 — Confirmation
- Summary of submitted activity
- Estimated verification timeline
- "What happens next" explanation of the pipeline
- CTA: "View my profile" + "Submit another"

## Component structure
```
apps/web/app/(app)/claim/
├── page.tsx           # Step router
├── components/
│   ├── StepIndicator.tsx
│   ├── Step1Type.tsx
│   ├── Step2Details.tsx
│   ├── Step3Evidence.tsx
│   ├── Step4AIReview.tsx
│   └── Step5Confirm.tsx
```

## Acceptance Criteria
- [ ] Step progress saved in state (going back doesn't lose data)
- [ ] File upload shows preview and size validation error
- [ ] Angel AI pre-review step shows spinner while checking
- [ ] Form cannot submit with required fields empty
- [ ] Successful submission shows confirmation with activity ID
- [ ] Mobile-friendly stepper (horizontal on desktop, vertical on mobile)
