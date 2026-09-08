import pytest
from intrinsiclab.service import analyze
from intrinsiclab.sensitivity import sensitivity_matrix


def test_more_discounting_reduces_value_for_positive_cash_flows(assumptions):
    matrix = sensitivity_matrix(assumptions, [.08,.1,.12], [.01,.02])
    assert matrix['rows'][0]['values'][0]['price'] > matrix['rows'][1]['values'][0]['price'] > matrix['rows'][2]['values'][0]['price']


def test_invalid_cell_is_unavailable_not_a_fabricated_price(assumptions):
    matrix = sensitivity_matrix(assumptions, [.02,.1], [.02])
    assert matrix['rows'][0]['values'][0]['price'] is None
    assert 'below WACC' in matrix['rows'][0]['values'][0]['reason']


def test_analysis_is_deterministic_and_carries_provenance(assumptions):
    a, b = analyze(assumptions), analyze(assumptions)
    assert a['model_id'] == b['model_id']
    assert a['source']['mode'] == 'DEMO DATA'
    assert a['interpretation']
    assert a['valuation']['price_per_share'] == pytest.approx(((13.3 + 13.464 / .08) / 1.1 - 15) / 10)
