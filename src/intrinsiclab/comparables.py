"""Relative valuation with compatible equity and enterprise denominators."""
from typing import Any
from pydantic import Field
from intrinsiclab.contracts import Contract, Finite, Nonnegative, Positive


class Comparable(Contract):
    company: str = Field(min_length=1, max_length=120)
    currency: str = Field(pattern=r'^[A-Z]{3}$')
    price: Nonnegative
    shares: Positive
    debt: Nonnegative
    cash: Nonnegative
    preferred_equity: Nonnegative = 0
    noncontrolling_interests: Nonnegative = 0
    revenue: Positive
    ebitda: Finite
    net_income: Finite
    book_equity: Finite


def _ratio(numerator: float, denominator: float) -> dict[str, Any]:
    if denominator <= 0:
        return {'value': None, 'reason': 'Nonpositive denominator; multiple is not meaningful'}
    if numerator < 0:
        return {'value': None, 'reason': 'Negative enterprise value; conventional multiple unavailable'}
    return {'value': numerator / denominator, 'reason': None}


def trading_multiples(peer: Comparable) -> dict[str, Any]:
    equity = peer.price * peer.shares
    enterprise = equity + peer.debt + peer.preferred_equity + peer.noncontrolling_interests - peer.cash
    # Earnings and book value belong to equity; sales and EBITDA finance every capital claimant.
    return {'company': peer.company, 'currency': peer.currency, 'market_equity': equity,
            'enterprise_value': enterprise, 'pe': _ratio(equity, peer.net_income),
            'ev_ebitda': _ratio(enterprise, peer.ebitda), 'ev_sales': _ratio(enterprise, peer.revenue),
            'price_book': _ratio(equity, peer.book_equity)}
