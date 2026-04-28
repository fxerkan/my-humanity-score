#!/usr/bin/env python3
"""
Fix migrated task files to match Backlog.md's required frontmatter schema.

Changes applied to each backlog/tasks/task-N - *.md:
  - Add `id: TASK-N` as first YAML field (if missing)
  - Rename created → created_date with YYYY-MM-DD HH:MM format
  - Rename updated → updated_date
  - Rename depends_on → dependencies
  - Add assignee: [] if missing
  - Strip the inline YAML comment line (# MHS-specific metadata …)
"""

import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
TASKS_DIR = ROOT / "backlog" / "tasks"
DRY_RUN = "--dry-run" in sys.argv

FRONTMATTER_RE = re.compile(r"^(---\n)(.*?)(\n---)", re.DOTALL)


def reformat_date(iso_str: str) -> str:
    iso_str = iso_str.strip().strip("'\"")
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return iso_str[:16].replace("T", " ")


def fix_task(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(raw)
    if not m:
        print(f"  SKIP (no frontmatter): {path.name}")
        return False

    fm = m.group(2)
    rest = raw[m.end():]

    task_num_match = re.search(r"task-(\d+)", path.name)
    task_num = int(task_num_match.group(1)) if task_num_match else 0
    task_id = f"TASK-{task_num}"

    # 1. Remove YAML comment lines (lines starting with #)
    fm = re.sub(r"^#[^\n]*\n?", "", fm, flags=re.MULTILINE)

    # 2. Add id field at the top if missing
    if not re.search(r"^id:", fm, re.MULTILINE):
        fm = f"id: {task_id}\n" + fm

    # 3. created → created_date
    def sub_created(mo):
        return f"created_date: '{reformat_date(mo.group(1))}'"
    fm = re.sub(r"^created:\s*(.+)$", sub_created, fm, flags=re.MULTILINE)

    # 4. updated → updated_date
    def sub_updated(mo):
        return f"updated_date: '{reformat_date(mo.group(1))}'"
    fm = re.sub(r"^updated:\s*(.+)$", sub_updated, fm, flags=re.MULTILINE)

    # 5. depends_on → dependencies
    fm = re.sub(r"^depends_on:", "dependencies:", fm, flags=re.MULTILINE)

    # 6. Add assignee if missing
    if not re.search(r"^assignee:", fm, re.MULTILINE):
        fm = re.sub(r"^(id:[^\n]+\n)", r"\1assignee: []\n", fm, flags=re.MULTILINE)

    # 7. Add dependencies if missing
    if not re.search(r"^dependencies:", fm, re.MULTILINE):
        fm = fm.rstrip("\n") + "\ndependencies: []\n"

    # Clean up extra blank lines
    fm = re.sub(r"\n{3,}", "\n\n", fm).strip("\n")

    new_content = f"---\n{fm}\n---{rest}"

    if new_content == raw:
        return False

    if not DRY_RUN:
        path.write_text(new_content, encoding="utf-8")
        print(f"  FIXED: {path.name}")
    else:
        print(f"  [DRY] {path.name} → id={task_id}")

    return True


def main():
    task_files = sorted(TASKS_DIR.glob("task-*.md"))
    print(f"{'DRY RUN — ' if DRY_RUN else ''}Fixing {len(task_files)} task frontmatters\n")
    fixed = sum(1 for f in task_files if fix_task(f))
    print(f"\nDone — {fixed}/{len(task_files)} files updated")


if __name__ == "__main__":
    main()
