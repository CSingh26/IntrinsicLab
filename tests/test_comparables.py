import pytest
from intrinsiclab.comparables import Comparable, trading_multiples


def peer(**overrides):
    return Comparable(**(dict(company='Peer', currency='USD', price=20, shares=10, debt=40,cash=10,revenue=100,ebitda=25,net_income=10,book_equity=80) | overrides))


def test_market_value_bridge_and_ratios():
    row = trading_multiples(peer())
    assert row['enterprise_value'] == 230
    assert row['pe']['value'] == 20
    assert row['ev_ebitda']['value'] == pytest.approx(9.2)
    assert row['price_book']['value'] == pytest.approx(2.5)


def test_losses_and_negative_book_do_not_produce_misleading_multiples():
    row = trading_multiples(peer(net_income=-5, book_equity=0,ebitda=-2))
    for metric in ['pe','price_book','ev_ebitda']:
        assert row[metric]['value'] is None
        assert row[metric]['reason']
