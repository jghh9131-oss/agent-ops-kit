#!/usr/bin/env python3
"""Append or inspect evidence rows in a markdown ledger. Offline. No network."""
from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Singapore")
HEADER = (
    "# Evidence ledger\n\n"
    "| Time (Asia/Singapore) | Kind | Amount | Currency | Note | Proof |\n"
    "|---|---|---|---|---|---|\n"
)
ROW_RE = re.compile(r"^\| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|\s*$")


def ensure_ledger(path: Path) -> None:
    if not path.exists():
        path.write_text(HEADER, encoding="utf-8")


def iter_rows(path: Path) -> list[tuple[str, str, str, str, str, str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        cells = m.groups()
        if cells[0].startswith("---") or cells[0].startswith("Time "):
            continue
        rows.append(cells)
    return rows


def main() -> None:
    p = argparse.ArgumentParser(description="Append or inspect an evidence ledger")
    p.add_argument("--ledger", required=True, help="Path to markdown ledger file")
    p.add_argument("--kind", choices=["income", "milestone", "feedback", "blocker"])
    p.add_argument("--note", help="What happened (one line)")
    p.add_argument("--amount", default="0", help="Amount if income (default 0)")
    p.add_argument("--currency", default="USD")
    p.add_argument("--proof", default="—", help="Path or URL to proof")
    p.add_argument("--list", action="store_true", help="Print existing rows")
    p.add_argument("--summary", action="store_true", help="Count rows by kind")
    args = p.parse_args()

    path = Path(args.ledger)
    ensure_ledger(path)

    if args.list or args.summary:
        rows = iter_rows(path)
        if args.summary:
            counts = Counter(r[1] for r in rows)
            print(f"rows={len(rows)}")
            for kind in ("income", "milestone", "feedback", "blocker"):
                print(f"{kind}: {counts.get(kind, 0)}")
        if args.list:
            for row in rows:
                print(" | ".join(row))
        if not args.kind:
            return

    if not args.kind or not args.note:
        raise SystemExit("append requires --kind and --note (or use --list / --summary)")

    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M %Z")
    note = args.note.replace("|", "/")
    row = f"| {now} | {args.kind} | {args.amount} | {args.currency} | {note} | {args.proof} |\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(row)
    print(f"appended -> {path}")
    print(row.strip())


if __name__ == "__main__":
    main()
