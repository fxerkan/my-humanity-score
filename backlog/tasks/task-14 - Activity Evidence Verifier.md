---
id: TASK-14
assignee: []
title: "Activity Evidence Verifier"
status: To Do
priority: high
labels: ["epic011-ml/ai-services", "sonnet", "developer"]
dependencies:
  - task-3
acceptance_criteria:
  - "OCR extracts text from a sample blood donation certificate correctly"
  - "NGO API lookup matches an Idealist volunteer entry (mocked in tests)"
  - "Low confidence (< 0.6) → returns `needs_peer_review` (not `rejected`)"
  - "Missing evidence → returns `needs_peer_review` immediately"
  - "External API timeouts handled (return `needs_peer_review`, not crash)"
  - "Processing time < 10 seconds for a typical PDF"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-011 ML/AI Services
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 30000
mhs_estimated_hours: 3
---

# TASK-014 — Activity Evidence Verifier (OCR + NGO API)

## Description
Service that validates activity evidence via OCR text extraction and
NGO/academic API lookups. Used by Verification Pipeline Layer 1 and Layer 2.

## OCR module
- Library: `pytesseract` (Tesseract 5) or Google Vision API fallback
- Input: image/PDF file path
- Output: extracted text + confidence score
- Post-processing: normalize whitespace, extract dates, org names, amounts

## NGO API lookups
```python
SUPPORTED_APIS = {
    "volunteer": ["idealist.org", "volunteerMatch.org", "unv.org"],
    "academic":  ["orcid.org", "crossref.org", "semanticscholar.org"],
    "ngo":       ["globalgiving.org", "guidestar.org"],
    "medical":   ["kizilay.org.tr", "redcross.org"],  # blood donation
}
```

## Verification logic
```python
def verify_evidence(activity_type, evidence_text, evidence_url):
    # 1. URL check → lookup in corresponding API
    # 2. Text check → NLP extraction of key entities
    # 3. Cross-reference: org name in text ↔ known NGO DB
    # Returns: VerificationResult(status, confidence, details)
```

## Internal API
```
POST /verify/evidence
Body: {
  "activity_id": "...",
  "activity_type": "humanitarian",
  "evidence_url": "https://...",
  "evidence_file_path": "/uploads/cert.pdf"
}
Response: {
  "status": "verified" | "needs_peer_review" | "rejected",
  "confidence": 0.91,
  "method": "ngo_api" | "ocr_ai" | "url_check",
  "details": "Found match in Idealist volunteer registry"
}
```

## Acceptance Criteria
- [ ] OCR extracts text from a sample blood donation certificate correctly
- [ ] NGO API lookup matches an Idealist volunteer entry (mocked in tests)
- [ ] Low confidence (< 0.6) → returns `needs_peer_review` (not `rejected`)
- [ ] Missing evidence → returns `needs_peer_review` immediately
- [ ] External API timeouts handled (return `needs_peer_review`, not crash)
- [ ] Processing time < 10 seconds for a typical PDF
