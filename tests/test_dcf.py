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


def test_exit_multiple_uses_final_ebitda_and_end_year_discount(assumptions):
    result = value_company(assumptions.model_copy(update={'terminal_method':'exit_multiple','exit_multiple':10}))
    assert result.terminal_value == pytest.approx(253)
    assert result.enterprise_value == pytest.approx((13.3 + 253) / 1.1)
    assert result.terminal_fcff is None


def test_negative_exit_ebitda_is_not_a_meaningful_multiple(assumptions):
    from intrinsiclab.contracts import OperatingYear
    with pytest.raises(ValueError, match='EBITDA'):
        value_company(assumptions.model_copy(update={'terminal_method':'exit_multiple','years':[OperatingYear(operating_margin=-.5)]}))
