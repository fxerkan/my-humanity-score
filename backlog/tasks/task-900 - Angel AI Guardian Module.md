---
id: TASK-900
assignee: []
title: "Angel AI Guardian Module"
status: To Do
priority: medium
labels: ["epic005-angel-ai-system", "sonnet", "developer", "post-mvp"]
dependencies:
  - task-12
acceptance_criteria:
  - "Known toxic text triggers HIGH/CRITICAL correctly"
  - "Hate speech always escalates to CRITICAL"
  - "PII detected and redacted suggestion returned"
  - "Fake profile scoring ≥ 0.7 flags to ethics board (tested with mock patterns)"
  - "All actions logged to `guardian_events` table for audit trail"
  - "Response time < 1 second for text analysis"
  - "No false positives on clearly benign content (manual test set)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-005 Angel AI System
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 45000
mhs_estimated_hours: 5
---

> **⏳ POST-MVP:** Bu modül MVP tamamlandıktan sonra geliştirilecek.

# TASK-015 — Angel AI Guardian Module

## Description
The Guardian module of Angel AI: detects and responds to threats in real-time.
Runs as a FastAPI service backed by toxic-BERT and pattern analysis.

## Threat types and detection

### 1. Toxicity (via TASK-012)
- Input: user-generated text (activity description, bio, comments)
- Threshold mapping: NONE/LOW/MEDIUM/HIGH/CRITICAL

### 2. Hate speech detection
- Classifier: fine-tuned BERT for hate speech (HatEval dataset)
- Automatic escalation to CRITICAL if hate speech detected

### 3. PII detection
- Patterns: email regex, phone regex, credit card Luhn check, TIN patterns
- Output: list of detected PII types + redacted text suggestion

### 4. Fake profile scoring
- Features: account age, activity frequency, similar-username pattern,
  suspicious verification success rate, IP diversity
- Threshold: score > 0.7 → flag for ethics board review

### 5. Coordinated attack detection
- Same IP submitting multiple activities in < 1 hour
- Multiple accounts following same pattern simultaneously
- Triggers: HIGH threat on pattern match

## Response actions per threat level
```python
THREAT_ACTIONS = {
    "NONE":     [],
    "LOW":      ["warn_user"],
    "MEDIUM":   ["filter_content", "warn_user"],
    "HIGH":     ["suspend_content", "notify_ethics_board"],
    "CRITICAL": ["block_account", "log_to_ethics_board", "notify_admin"],
}
```

## API
```
POST /guardian/analyze
Body: { "user_id": "...", "content": "...", "context": "activity_description" }
Response: {
  "threat_level": "LOW",
  "threats_detected": ["toxicity"],
  "actions_taken": ["warn_user"],
  "message_to_user": "Your content was flagged. Please review..."
}
```

## Acceptance Criteria
- [ ] Known toxic text triggers HIGH/CRITICAL correctly
- [ ] Hate speech always escalates to CRITICAL
- [ ] PII detected and redacted suggestion returned
- [ ] Fake profile scoring ≥ 0.7 flags to ethics board (tested with mock patterns)
- [ ] All actions logged to `guardian_events` table for audit trail
- [ ] Response time < 1 second for text analysis
- [ ] No false positives on clearly benign content (manual test set)
