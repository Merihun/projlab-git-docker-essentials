"""Revenue per country from the orders CSV."""

from __future__ import annotations

import csv
from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from report.settings import CURRENCY, DECIMALS


def summarise(rows) -> list[tuple[str, int, Decimal]]:
    """``(country, orders, revenue)`` for orders that are not cancelled, highest revenue first."""
    orders: dict[str, int] = defaultdict(int)
    revenue: dict[str, Decimal] = defaultdict(Decimal)
    for row in rows:
        if row["status"] == "cancelled":
            continue
        orders[row["country"]] += 1
        revenue[row["country"]] += int(row["quantity"]) * Decimal(row["unit_price"])
    step = Decimal(1).scaleb(-DECIMALS)
    out = [(c, orders[c], revenue[c].quantize(step, ROUND_HALF_UP)) for c in revenue]
    return sorted(out, key=lambda r: (-r[2], r[0]))


def write(summary, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["country", "orders", f"revenue_{CURRENCY.lower()}"])
        writer.writerows(summary)


def to_postgres(summary, url: str) -> int:
    """Replace the table report.country_revenue with ``summary``. Needs psycopg (in report/requirements.txt)."""
    import psycopg

    with psycopg.connect(url) as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS report")
        conn.execute("CREATE TABLE IF NOT EXISTS report.country_revenue (country text PRIMARY KEY, orders int, revenue numeric(14, 2))")
        conn.execute("TRUNCATE report.country_revenue")
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO report.country_revenue VALUES (%s, %s, %s)", summary)
    return len(summary)
