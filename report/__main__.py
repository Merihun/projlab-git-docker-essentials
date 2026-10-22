"""python -m report IN.csv OUT.csv [--postgres]

Writes revenue per country to OUT.csv. With --postgres it also replaces report.country_revenue in the database
named by DATABASE_URL.
"""

import csv
import os
import sys
from pathlib import Path

from report.summary import summarise, to_postgres, write


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        return 2
    source, target = Path(args[0]), Path(args[1])
    if not source.is_file():
        print(f"no such file: {source}", file=sys.stderr)
        return 1
    with source.open(newline="") as handle:
        summary = summarise(csv.DictReader(handle))
    write(summary, target)
    print(f"wrote {len(summary)} countries to {target}")
    if "--postgres" in argv:
        url = os.environ.get("DATABASE_URL")
        if not url:
            print("--postgres needs DATABASE_URL", file=sys.stderr)
            return 2
        print(f"replaced report.country_revenue: {to_postgres(summary, url)} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
