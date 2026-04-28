---
id: TASK-903
title: 'hotfix: fix CI ruff lint failures in conftest.py and seed_demo.py'
status: Done
assignee: []
created_date: '2026-04-28 13:00'
labels:
  - bug
  - ci
  - hotfix
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
GitHub Actions CI was failing on the `API (Python)` job due to 4 ruff lint errors that caused `ruff check .` to exit with code 1.\n\nErrors found:\n- `tests/conftest.py`: unused imports `typing.Any` and `unittest.mock.AsyncMock` (F401)\n- `scripts/seed_demo.py`: unsorted import block (I001) and f-string without placeholders (F541)\n\nAll 4 errors are auto-fixable and were resolved with `ruff check . --fix`.\n\nCI run: https://github.com/fxerkan/my-humanity-score/actions/runs/25051507925
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 CI `API (Python)` job passes `ruff check .` with zero errors
- [ ] #2 No regressions introduced to conftest.py or seed_demo.py behaviour
<!-- AC:END -->
