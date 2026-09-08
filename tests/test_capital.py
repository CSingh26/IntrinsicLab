import pytest
from intrinsiclab.capital import cost_of_capital
from intrinsiclab.contracts import CapitalStructure


def funding(**overrides):
    values = dict(equity_market_value=800, debt_market_value=200, risk_free_rate=.04, beta=1.2, equity_risk_premium=.05, pretax_cost_of_debt=.06, tax_rate=.25)
    return CapitalStructure(**(values | overrides))


def test_market_weights_and_interest_tax_shield():
    result = cost_of_capital(funding())
    assert result['cost_of_equity'] == pytest.approx(.1)
    assert result['wacc'] == pytest.approx(.089)


def test_no_financing_is_undefined():
    with pytest.raises(ValueError, match='financing'):
        cost_of_capital(funding(equity_market_value=0, debt_market_value=0))


def test_unlevered_wacc_equals_cost_of_equity():
    assert cost_of_capital(funding(debt_market_value=0))['wacc'] == pytest.approx(.1)
