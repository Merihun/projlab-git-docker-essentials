"""The report's own tests: they run on your machine, in the container and in CI."""

from decimal import Decimal

from report.summary import summarise


def row(country, quantity, price, status="paid"):
    return {"country": country, "quantity": str(quantity), "unit_price": price, "status": status}


def test_revenue_per_country_highest_first():
    out = summarise([row("FR", 1, "10.00"), row("GB", 2, "10.00"), row("GB", 1, "5.00")])
    assert out == [("GB", 2, Decimal("25.00")), ("FR", 1, Decimal("10.00"))]


def test_cancelled_orders_do_not_count():
    assert summarise([row("GB", 3, "9.99", "cancelled")]) == []
