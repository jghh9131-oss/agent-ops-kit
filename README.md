# agent-ops-kit（preview）

Offline operator kit for solo builders: evidence ledger, pre-publish checklist, fee estimator, secret scan, and storefront templates.

## Buy
**agent-ops-kit v0.2** — $9 USD, one-time: [https://brtr-b.itch.io/agent-ops-kit](https://brtr-b.itch.io/agent-ops-kit)

## Quick start (after purchase / with local copy)
```bash
python3 scripts/selftest.py
python3 scripts/fee_estimate.py --price 9 --intl --sources
python3 scripts/evidence_log.py --ledger examples/sample-ledger.md --kind milestone --note "first run"
```

No paid APIs. Scripts run offline.

## What’s in the paid zip
See product README inside the download. This public preview may ship a subset or docs-only of the paid pack.

## License
Personal evaluation of preview materials OK. Redistribution of the paid pack requires purchase.


## Preview scripts in this repo
```bash
python3 scripts/fee_estimate.py --price 9 --intl --sources
python3 scripts/release_checklist.py --out /tmp/checklist.md
python3 scripts/evidence_log.py --ledger examples/sample-ledger.md --kind milestone --note "cloned preview"
```

Full paid pack (**agent-ops-kit v0.2**, $9 USD one-time): [https://brtr-b.itch.io/agent-ops-kit](https://brtr-b.itch.io/agent-ops-kit)
