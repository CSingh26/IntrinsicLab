import pytest
from intrinsiclab.dcf import value_company


def test_perpetuity_reinvestment_and_value_bridge(assumptions):
    result = value_company(assumptions)
    terminal_fcff = 110 * 1.02 * .2 * .75 * (1 - .02 / .1)
    ev = (13.3 + terminal_fcff / .08) / 1.1
    assert result.terminal_fcff == pytest.approx(terminal_fcff)
    assert result.enterprise_value == pytest.approx(ev)
    assert result.equity_value == pytest.approx(ev - 15)
    assert result.price_per_share == pytest.approx((ev - 15) / 10)


@pytest.mark.parametrize('updates', [{'terminal_growth':.1}, {'terminal_roic':.01}])
def test_rejects_unstable_terminal_assumptions(assumptions, updates):
    with pytest.raises(ValueError):
        value_company(assumptions.model_copy(update=updates))


def test_debt_does_not_get_hidden_by_equity_floor(assumptions):
    result = value_company(assumptions.model_copy(update={'debt':1e6}))
    assert result.equity_value < 0
    assert result.price_per_share < 0
