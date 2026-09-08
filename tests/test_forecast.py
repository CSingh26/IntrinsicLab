import pytest
from intrinsiclab.forecast import project_cash_flows
from intrinsiclab.contracts import OperatingYear


def test_operating_cash_flow_bridge(assumptions):
    row = project_cash_flows(assumptions)[0]
    assert row.revenue == pytest.approx(110)
    assert row.nopat == pytest.approx(16.5)
    assert row.change_nwc == pytest.approx(1)
    assert row.fcff == pytest.approx(13.3)
    assert row.ebitda == pytest.approx(25.3)
    assert row.year == 2026


def test_negative_profit_does_not_create_immediate_tax_cash(assumptions):
    model = assumptions.model_copy(update={'years':[OperatingYear(operating_margin=-.1)]})
    row = project_cash_flows(model)[0]
    assert row.cash_taxes == 0
    assert row.nopat == row.ebit


def test_changes_use_previous_year_nwc(assumptions):
    model = assumptions.model_copy(update={'years': assumptions.years * 2})
    assert project_cash_flows(model)[1].change_nwc == pytest.approx(1.1)
