#!/usr/bin/env python3
"""Run offline demos for every script in this kit."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(args: list[str]) -> str:
    proc = subprocess.run(args, check=True, capture_output=True, text=True)
    return proc.stdout


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="aok-selftest-") as tmp:
        tmp_path = Path(tmp)
        ledger = tmp_path / "ledger.md"
        checklist = tmp_path / "checklist.md"

        out = run([sys.executable, str(HERE / "evidence_log.py"),
                   "--ledger", str(ledger), "--kind", "milestone",
                   "--note", "selftest append"])
        assert "appended" in out

        out = run([sys.executable, str(HERE / "evidence_log.py"),
                   "--ledger", str(ledger), "--summary", "--list"])
        assert "milestone: 1" in out

        out = run([sys.executable, str(HERE / "release_checklist.py"),
                   "--out", str(checklist)])
        assert "wrote" in out

        out = run([sys.executable, str(HERE / "release_checklist.py"),
                   "--file", str(checklist), "--mark", "1", "--status"])
        assert "done=1/8" in out

        out = run([sys.executable, str(HERE / "fee_estimate.py"),
                   "--price", "9", "--intl"])
        assert "Polar Starter" in out
        assert "$7.91" in out  # 9 - (0.45+0.50) - 0.135 = 7.915 -> $7.91

        out = run([sys.executable, str(HERE / "secrets_scan.py"), "--root", str(ROOT)])
        assert out.startswith("clean:")

    print("selftest OK")
    print(f"kit root: {ROOT}")


if __name__ == "__main__":
    main()
