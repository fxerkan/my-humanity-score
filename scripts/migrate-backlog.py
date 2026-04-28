#!/usr/bin/env python3
"""
Migrate existing MHS backlog to Backlog.md format.

Changes:
  backlog/tasks/task-XXX-*.md  →  backlog/task-N - Title.md  (Backlog.md convention)
  backlog/epics/*.md           →  backlog/docs/epics/*.md
  backlog/sprints/*.md         →  backlog/docs/sprints/*.md

Run: python scripts/migrate-backlog.py [--dry-run]
"""

import os
import re
import sys
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List

DRY_RUN = "--dry-run" in sys.argv
ROOT = Path(__file__).parent.parent
BACKLOG = ROOT / "backlog"
TASKS_SRC = BACKLOG / "tasks"
EPICS_SRC = BACKLOG / "epics"
SPRINTS_SRC = BACKLOG / "sprints"

DOCS_EPICS = BACKLOG / "docs" / "epics"
DOCS_SPRINTS = BACKLOG / "docs" / "sprints"

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Status mapping ────────────────────────────────────────────────────────────
STATUS_MAP = {
    "ready": "To Do",
    "blocked": "To Do",
    "planned": "To Do",
    "draft": "To Do",
    "in-progress": "In Progress",
    "in_progress": "In Progress",
    "done": "Done",
    "completed": "Done",
    "in-review": "In Progress",
}

# ── Priority mapping ─────────────────────────────────────────────────────────
PRIORITY_MAP = {
    "P0": "high",
    "P1": "high",
    "P2": "medium",
    "P3": "low",
}

# ── Model → label mapping ─────────────────────────────────────────────────────
MODEL_LABEL_MAP = {
    "claude-haiku-4-5": "haiku",
    "claude-haiku-4-5-20251001": "haiku",
    "claude-sonnet-4-6": "sonnet",
    "claude-opus-4-6": "opus",
    "gemini-2.5-pro": "gemini-pro",
}


def slugify(text: str) -> str:
    """Create a filesystem-safe short slug."""
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    # Keep it short for filenames
    words = text.split("-")[:8]
    return "-".join(words)


def extract_field(content: str, *field_names: str) -> Optional[str]:
    """Extract **Field:** value from markdown body (our old metadata format)."""
    for name in field_names:
        pattern = rf"\*\*{re.escape(name)}:\*\*\s*`?([^`\n]+)`?"
        m = re.search(pattern, content, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def extract_h1_title(content: str) -> str:
    """Extract title from the first H1 heading."""
    m = re.search(r"^#\s+(?:TASK-\d+\s*[—-]\s*)?(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "Untitled"


def extract_task_number(filename: str) -> int:
    """Extract the numeric ID from task-001-*.md → 1."""
    m = re.search(r"task-(\d+)", filename)
    return int(m.group(1)) if m else 0


def extract_deps(content: str) -> List[str]:
    """Extract dependency list from metadata block or YAML-like field."""
    # Old format: "- **Dependencies:** TASK-002, TASK-003"
    m = re.search(r"\*\*Dep[^:]*:\*\*\s*(.+)", content, re.IGNORECASE)
    if not m:
        return []
    raw = m.group(1).strip()
    # Parse comma-separated or "none"
    if re.match(r"none|—|-$", raw, re.IGNORECASE):
        return []
    deps = re.findall(r"TASK-(\d+)", raw, re.IGNORECASE)
    return [f"task-{int(d)}" for d in deps]


def extract_acceptance_criteria(content: str) -> List[str]:
    """Extract acceptance criteria checklist items from the body."""
    section = re.search(
        r"##\s+Acceptance Criteria\s*\n(.*?)(?=\n##|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if not section:
        return []
    items = re.findall(r"-\s+\[[ x]\]\s+(.+)", section.group(1))
    return [item.strip() for item in items[:10]]  # cap at 10 for frontmatter


def strip_old_metadata_block(content: str) -> str:
    """Remove the ## Metadata section (now in frontmatter)."""
    content = re.sub(
        r"##\s+Metadata\s*\n(?:-\s+\*\*[^*]+\*\*[^\n]*\n)+\n?",
        "",
        content,
        flags=re.IGNORECASE,
    )
    return content


def build_frontmatter(
    title: str,
    status_raw: str,
    priority_raw: str,
    agent: str,
    model: str,
    epic: str,
    deps: List[str],
    est_tokens: str,
    est_hours: str,
    ac_items: List[str],
    extra_labels: List[str],
) -> str:
    status = STATUS_MAP.get(status_raw.lower(), "To Do")
    priority = PRIORITY_MAP.get(priority_raw, "medium")
    model_label = MODEL_LABEL_MAP.get(model.strip(), "")

    labels = []
    if epic:
        labels.append(epic.lower().replace("epic-", "epic").replace(" ", "-"))
    if model_label:
        labels.append(model_label)
    if agent:
        labels.append(agent.lower().replace(" ", "-"))
    labels.extend(extra_labels)

    labels_str = ", ".join(f'"{l}"' for l in labels) if labels else ""
    deps_str = "\n".join(f"  - {d}" for d in deps) if deps else ""
    ac_str = "\n".join(f'  - "{a}"' for a in ac_items) if ac_items else ""

    lines = ["---", f'title: "{title}"', f"status: {status}", f"priority: {priority}"]

    if labels_str:
        lines.append(f"labels: [{labels_str}]")
    if deps:
        lines.append(f"depends_on:\n{deps_str}")
    if ac_items:
        lines.append(f"acceptance_criteria:\n{ac_str}")

    lines += [
        f"created: {NOW}",
        f"updated: {NOW}",
        "# MHS-specific metadata (preserved for agent routing)",
    ]
    if epic:
        lines.append(f"mhs_epic: {epic}")
    if agent:
        lines.append(f"mhs_agent: {agent}")
    if model:
        lines.append(f"mhs_model: {model}")
    if est_tokens:
        lines.append(f"mhs_estimated_tokens: {est_tokens.replace(',','').replace('~','').strip()}")
    if est_hours:
        hours = re.search(r"(\d+)", est_hours)
        if hours:
            lines.append(f"mhs_estimated_hours: {hours.group(1)}")

    lines.append("---")
    return "\n".join(lines)


def migrate_task(src: Path) -> Optional[Path]:
    """Convert one task file to Backlog.md format. Returns destination path."""
    raw = src.read_text(encoding="utf-8")

    task_num = extract_task_number(src.name)
    title = extract_h1_title(raw)
    status_raw = extract_field(raw, "Status") or "ready"
    priority_raw = extract_field(raw, "Priority") or "P2"
    agent = extract_field(raw, "Agent") or ""
    model = extract_field(raw, "Model") or ""
    epic = extract_field(raw, "Epic") or ""
    est_tokens = extract_field(raw, "Estimated tokens") or ""
    est_hours = extract_field(raw, "Estimated time") or ""
    deps = extract_deps(raw)
    ac_items = extract_acceptance_criteria(raw)

    # Clean title: remove trailing punctuation from heading
    title_clean = re.sub(r"[()—\-]+$", "", title).strip()

    frontmatter = build_frontmatter(
        title=title_clean,
        status_raw=status_raw,
        priority_raw=priority_raw,
        agent=agent,
        model=model,
        epic=epic,
        deps=deps,
        est_tokens=est_tokens,
        est_hours=est_hours,
        ac_items=ac_items,
        extra_labels=[],
    )

    # Clean body: remove old metadata block, keep rest
    body = strip_old_metadata_block(raw)
    # Remove old H1 title line (we keep it in the body for readability)
    new_content = f"{frontmatter}\n\n{body.lstrip()}"

    # Destination filename: "task-N - Title.md"
    # Sanitize: replace filesystem-unsafe chars, fix open parens from truncation
    safe_title = title_clean.replace("/", "-").replace("\\", "-").replace(":", "-")
    slug = safe_title[:60]
    # If truncation left an unmatched open paren, strip from it
    if slug.count("(") > slug.count(")"):
        slug = slug[:slug.rfind("(")].rstrip(" ")
    dest_name = f"task-{task_num} - {slug}.md"
    dest = BACKLOG / dest_name

    print(f"  {'[DRY] ' if DRY_RUN else ''}{src.name} → {dest_name}")

    if not DRY_RUN:
        dest.write_text(new_content, encoding="utf-8")

    return dest


def migrate_docs(src_dir: Path, dest_dir: Path, label: str) -> None:
    """Move doc files (epics, sprints) to backlog/docs/<subdir>/."""
    if not src_dir.exists():
        print(f"  Skipping {src_dir} (not found)")
        return
    if not DRY_RUN:
        dest_dir.mkdir(parents=True, exist_ok=True)

    for f in sorted(src_dir.glob("*.md")):
        dest = dest_dir / f.name
        print(f"  {'[DRY] ' if DRY_RUN else ''}{f.relative_to(ROOT)} → {dest.relative_to(ROOT)}")
        if not DRY_RUN:
            shutil.copy2(f, dest)


def main() -> None:
    print(f"{'DRY RUN — ' if DRY_RUN else ''}Migrating MHS backlog to Backlog.md format")
    print(f"Root: {ROOT}\n")

    # 1. Migrate task files
    task_files = sorted(TASKS_SRC.glob("task-*.md"))
    print(f"── Tasks ({len(task_files)} files) ──────────────────────────────")
    for src in task_files:
        migrate_task(src)

    # 2. Move epics → docs/epics/
    print(f"\n── Epics → docs/epics/ ─────────────────────────────────────────")
    migrate_docs(EPICS_SRC, DOCS_EPICS, "epic")

    # 3. Move sprints → docs/sprints/
    print(f"\n── Sprints → docs/sprints/ ─────────────────────────────────────")
    migrate_docs(SPRINTS_SRC, DOCS_SPRINTS, "sprint")

    # 4. Remove old directories if not dry run
    if not DRY_RUN:
        for old_dir in [TASKS_SRC, EPICS_SRC, SPRINTS_SRC]:
            if old_dir.exists():
                shutil.rmtree(old_dir)
                print(f"\n  Removed old directory: {old_dir.relative_to(ROOT)}/")

    print(f"\n{'[DRY RUN complete]' if DRY_RUN else '✅ Migration complete!'}")
    if not DRY_RUN:
        print("  Next: run `backlog board` or `backlog browser` to verify.")


if __name__ == "__main__":
    main()
