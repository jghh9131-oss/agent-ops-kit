#!/usr/bin/env python3
"""Estimate net proceeds after published platform fees. Offline. No network.

Rates checked 2026-11-08 against official pages (see --sources).
Polar VAT note: Polar's published Sweden example applies plan % and the
international-card extra to (price + VAT), not list price alone.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


CENTS = Decimal("0.01")


def d(n: float | Decimal) -> Decimal:
    return Decimal(str(n)).quantize(CENTS, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Quote:
    name: str
    gross: Decimal
    fee: Decimal
    extra: Decimal
    net: Decimal
    notes: str
    source: str


def money(n: Decimal) -> str:
    return f"${n.quantize(CENTS, rounding=ROUND_HALF_UP)}"


def polar(price: float, pct: float, fixed: float, intl: bool, vat_rate: float, name: str, source: str) -> Quote:
    price_d = d(price)
    charge = d(price_d + d(price) * Decimal(str(vat_rate)))
    fee = d(charge * Decimal(str(pct)) + Decimal(str(fixed)))
    extra = d(charge * Decimal("0.015")) if intl else d(0)
    notes = f"charge_base={money(charge)} (list + VAT {vat_rate:.0%})"
    if intl:
        notes += "; +1.5% international card"
    return Quote(name, price_d, fee, extra, d(price_d - fee - extra), notes, source)


def gumroad(price: float, pct: float, fixed: float, name: str, source: str) -> Quote:
    price_d = d(price)
    fee = d(price_d * Decimal(str(pct)) + Decimal(str(fixed)))
    return Quote(name, price_d, fee, d(0), d(price_d - fee), "fees on list price", source)


def itch(price: float, share: float, source: str) -> Quote:
    price_d = d(price)
    platform = d(price_d * Decimal(str(share)))
    processor = d(price_d * Decimal("0.029") + Decimal("0.30"))
    fee = d(platform + processor)
    notes = f"itch share {share:.0%} + processor 2.9%+$0.30"
    return Quote("itch.io", price_d, fee, d(0), d(price_d - fee), notes, source)


def main() -> None:
    p = argparse.ArgumentParser(description="Estimate seller net after published fees")
    p.add_argument("--price", type=float, required=True, help="List price in USD")
    p.add_argument("--intl", action="store_true", help="Apply Polar +1.5% international-card extra")
    p.add_argument("--vat-rate", type=float, default=0.0, help="VAT rate added on top before Polar fees (e.g. 0.25)")
    p.add_argument("--itch-share", type=float, default=0.10, help="itch.io platform share (docs example default 10%)")
    p.add_argument("--sources", action="store_true", help="Print rate sources")
    args = p.parse_args()

    if args.price <= 0:
        raise SystemExit("price must be > 0")
    if not (0.0 <= args.itch_share <= 1.0):
        raise SystemExit("itch-share must be between 0 and 1")

    polar_src = "https://polar.sh/resources/pricing (checked 2026-11-08)"
    gum_src = "https://gumroad.com/pricing (checked 2026-11-08)"
    itch_src = "https://itch.io/docs/creators/payments (checked 2026-11-08)"

    quotes = [
        polar(args.price, 0.05, 0.50, args.intl, args.vat_rate, "Polar Starter", polar_src),
        polar(args.price, 0.038, 0.40, args.intl, args.vat_rate, "Polar Pro (excludes $20/mo)", polar_src),
        gumroad(args.price, 0.10, 0.50, "Gumroad Direct", gum_src),
        gumroad(args.price, 0.30, 0.00, "Gumroad Discover", gum_src),
        itch(args.price, args.itch_share, itch_src),
    ]

    print("| Platform | Gross | Platform+processor fee | Extra | Est. net | Notes |")
    print("|---|---:|---:|---:|---:|---|")
    for q in quotes:
        print(f"| {q.name} | {money(q.gross)} | {money(q.fee)} | {money(q.extra)} | {money(q.net)} | {q.notes} |")
    print()
    print("Not included: Polar Stripe payout fees ($2/active payout month + 0.25%+$0.25 per payout; FX 0.25%–1%).")
    print("Polar new orgs (on/after 2026-05-12): ~7-day settlement; USD payout minimum $10.")
    print("These are estimates from public rate pages, not invoices.")
    if args.sources:
        print()
        for q in quotes:
            print(f"- {q.name}: {q.source}")


if __name__ == "__main__":
    main()
