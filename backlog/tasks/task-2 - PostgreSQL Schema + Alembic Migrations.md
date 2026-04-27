---
id: TASK-2
milestone: "M1: Dev Environment"
assignee: []
title: "PostgreSQL Schema + Alembic Migrations"
status: To Do
priority: high
labels: ["epic001-foundation-&-infrastructure", "sonnet", "developer"]
dependencies:
  - task-1
acceptance_criteria:
  - "`alembic upgrade head` creates all tables without errors"
  - "`alembic downgrade -1` reverses cleanly"
  - "All foreign keys have cascade rules defined"
  - "Soft delete pattern (`deleted_at`) applied to `users`"
  - "`updated_at` auto-updates via trigger on `users` and `activities`"
  - "No plain-text tokens in `connected_platforms` (column clearly named `_encrypted`)"
created_date: '2026-04-27 13:41'
updated_date: '2026-04-27 13:41'
mhs_epic: EPIC-001 Foundation & Infrastructure
mhs_agent: Developer
mhs_model: claude-sonnet-4-6
mhs_estimated_tokens: 20000
mhs_estimated_hours: 2
---

# TASK-002 — PostgreSQL Schema + Alembic Migrations

## Description
Create the full PostgreSQL database schema from concept/MHS_KB_02_Technical.md
and wire up Alembic for migrations. This schema is the source of truth for all
backend models.

## Tables to create

### users
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
email VARCHAR(255) UNIQUE NOT NULL,
username VARCHAR(50) UNIQUE NOT NULL,
password_hash VARCHAR(255),
display_name VARCHAR(100),
bio TEXT,
location VARCHAR(100),
birth_year SMALLINT,
profession VARCHAR(100),
profile_public BOOLEAN DEFAULT true,
show_score BOOLEAN DEFAULT true,
show_activities BOOLEAN DEFAULT true,
created_at TIMESTAMPTZ DEFAULT NOW(),
updated_at TIMESTAMPTZ DEFAULT NOW(),
deleted_at TIMESTAMPTZ  -- soft delete
```

### mhs_scores
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
user_id UUID REFERENCES users(id),
social_impact NUMERIC(6,2) DEFAULT 0,
environmental NUMERIC(6,2) DEFAULT 0,
knowledge_innovation NUMERIC(6,2) DEFAULT 0,
economic NUMERIC(6,2) DEFAULT 0,
cultural_artistic NUMERIC(6,2) DEFAULT 0,
civic_political NUMERIC(6,2) DEFAULT 0,
-- hidden factors (stored but never sent raw to client)
carbon_penalty NUMERIC(6,2) DEFAULT 0,
toxicity_penalty NUMERIC(6,2) DEFAULT 0,
network_multiplier NUMERIC(4,3) DEFAULT 1.0,
consistency_multiplier NUMERIC(4,3) DEFAULT 1.0,
geographic_multiplier NUMERIC(4,3) DEFAULT 1.0,
final_score NUMERIC(6,2) DEFAULT 0,
score_level VARCHAR(30),
global_percentile NUMERIC(5,2),
calculated_at TIMESTAMPTZ DEFAULT NOW()
```

### activities
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
user_id UUID REFERENCES users(id),
type VARCHAR(50) NOT NULL,  -- 'humanitarian','science','community','environment','education'
title VARCHAR(255) NOT NULL,
description TEXT,
evidence_url TEXT,
evidence_file_path TEXT,
verification_status VARCHAR(20) DEFAULT 'pending',  -- pending|auto_verified|peer_review|verified|rejected
impact_score NUMERIC(6,2) DEFAULT 0,
category VARCHAR(50),
activity_date DATE,
visibility VARCHAR(20) DEFAULT 'public',  -- public|followers|private
created_at TIMESTAMPTZ DEFAULT NOW(),
updated_at TIMESTAMPTZ DEFAULT NOW()
```

### connected_platforms
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
user_id UUID REFERENCES users(id),
platform VARCHAR(50) NOT NULL,  -- 'github','linkedin','twitter'
platform_user_id VARCHAR(255),
access_token_encrypted TEXT,
refresh_token_encrypted TEXT,
token_expires_at TIMESTAMPTZ,
sync_frequency VARCHAR(20) DEFAULT 'weekly',
last_synced_at TIMESTAMPTZ,
connected_at TIMESTAMPTZ DEFAULT NOW()
```

### badges (awarded)
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
user_id UUID REFERENCES users(id),
badge_type VARCHAR(50) NOT NULL,
badge_layer SMALLINT NOT NULL,  -- 1,2,3,4
awarded_at TIMESTAMPTZ DEFAULT NOW(),
UNIQUE(user_id, badge_type)
```

### groups
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
name VARCHAR(100) NOT NULL,
slug VARCHAR(100) UNIQUE NOT NULL,
description TEXT,
type VARCHAR(20) NOT NULL,  -- open|closed|thematic|local|corporate
theme VARCHAR(50),
location VARCHAR(100),
privacy VARCHAR(20) DEFAULT 'public',
collective_mhs NUMERIC(8,2) DEFAULT 0,
member_count INTEGER DEFAULT 0,
created_by UUID REFERENCES users(id),
created_at TIMESTAMPTZ DEFAULT NOW()
```

## Alembic setup
- Initialize `alembic/` in `apps/api/`
- Create initial migration with all tables above
- Add `updated_at` trigger function for auto-update
- Add indexes: `users(email)`, `users(username)`, `activities(user_id)`,
  `mhs_scores(user_id)`, `activities(verification_status)`

## Acceptance Criteria
- [ ] `alembic upgrade head` creates all tables without errors
- [ ] `alembic downgrade -1` reverses cleanly
- [ ] All foreign keys have cascade rules defined
- [ ] Soft delete pattern (`deleted_at`) applied to `users`
- [ ] `updated_at` auto-updates via trigger on `users` and `activities`
- [ ] No plain-text tokens in `connected_platforms` (column clearly named `_encrypted`)
