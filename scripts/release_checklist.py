#!/usr/bin/env python3
"""Emit or update a zero-budget digital release checklist. Offline."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ITEMS = [
    "Product zip opens; README has install/run steps that work offline",
    "Price >= platform fee floor (avoid sub-$2 if card fixed fees apply)",
    "Checkout / Buy URL placeholder ready in public README",
    "No copyrighted third-party assets without license",
    "No secrets, keys, private data in the zip",
    "Human approved: storefront account + payout KYC",
    "Human approved: any public post or outreach message",
    "Evidence folder path decided for first Paid order screenshot",
]
ITEM_RE = re.compile(r"^- \[([ xX])\] (.+)$")


def render(done: list[bool] | None = None) -> str:
    flags = done or [False] * len(ITEMS)
    lines = ["# Pre-publish checklist", ""]
    for i, (item, is_done) in enumerate(zip(ITEMS, flags), start=1):
        mark = "x" if is_done else " "
        lines.append(f"- [{mark}] {item}")
    lines.append("")
    return "\n".join(lines)


def parse(path: Path) -> list[tuple[bool, str]]:
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ITEM_RE.match(line)
        if m:
            found.append((m.group(1).lower() == "x", m.group(2)))
    return found


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", help="Write a fresh checklist markdown to this path")
    p.add_argument("--file", help="Existing checklist to inspect or update")
    p.add_argument("--mark", type=int, help="1-based item number to mark done")
    p.add_argument("--unmark", type=int, help="1-based item number to mark not done")
    p.add_argument("--status", action="store_true", help="Print done/total")
    args = p.parse_args()

    if args.out:
        Path(args.out).write_text(render(), encoding="utf-8")
        print(f"wrote {args.out}")
        print(render())
        return

    if not args.file:
        print(render())
        return

    path = Path(args.file)
    if not path.exists():
        path.write_text(render(), encoding="utf-8")

    parsed = parse(path)
    # Align to canonical items; keep marks when text matches
    done = [False] * len(ITEMS)
    by_text = {text: is_done for is_done, text in parsed}
    for i, item in enumerate(ITEMS):
        done[i] = by_text.get(item, False)

    def check_index(n: int) -> int:
        if n < 1 or n > len(ITEMS):
            raise SystemExit(f"item must be 1..{len(ITEMS)}")
        return n - 1

    changed = False
    if args.mark:
        done[check_index(args.mark)] = True
        changed = True
    if args.unmark:
        done[check_index(args.unmark)] = False
        changed = True
    if changed:
        path.write_text(render(done), encoding="utf-8")
        print(f"updated {path}")

    if args.status or changed:
        total = len(ITEMS)
        n_done = sum(done)
        print(f"done={n_done}/{total}")
        for i, (item, is_done) in enumerate(zip(ITEMS, done), start=1):
            print(f"{i}. [{'x' if is_done else ' '}] {item}")
        return

    print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
