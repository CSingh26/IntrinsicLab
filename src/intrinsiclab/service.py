"""Interpretation is derived only from validated, reproducible calculations."""
import hashlib
from typing import Any
from intrinsiclab.contracts import ValuationAssumptions
from intrinsiclab.dcf import value_company
from intrinsiclab.sensitivity import sensitivity_matrix


def analyze(model: ValuationAssumptions) -> dict[str, Any]:
    valuation = value_company(model)
    warnings = []
    terminal_share = valuation.terminal_share_of_ev
    if terminal_share is not None and terminal_share > .75:
        warnings.append('More than 75% of enterprise value comes from terminal assumptions.')
    if valuation.equity_value < 0:
        warnings.append('Capital claims exceed modeled enterprise value; the equity residual is negative.')
    if any(row.fcff < 0 for row in valuation.forecast):
        warnings.append('The explicit forecast includes cash outflows; investigate reinvestment and liquidity.')
    if model.terminal_growth < 0 and model.terminal_method == 'gordon':
        warnings.append('Negative terminal growth assumes cash-releasing disinvestment indefinitely.')
    if model.terminal_method == 'gordon' and model.wacc - model.terminal_growth < .02:
        warnings.append('A narrow WACC–growth spread makes terminal value extremely sensitive.')
    columns = ([model.terminal_growth + offset for offset in [-.01,-.005,0,.005,.01]]
               if model.terminal_method == 'gordon'
               else [model.exit_multiple * factor for factor in [.6,.8,1,1.2,1.4]])
    matrix = sensitivity_matrix(model, [model.wacc + x for x in [-.02,-.01,0,.01,.02]], columns)
    prices = [c['price'] for r in matrix['rows'] for c in r['values'] if c['price'] is not None]
    return {'model_id': hashlib.sha256(model.model_dump_json().encode()).hexdigest()[:16],
            'engine_version': '1.0.0', 'source': model.source.model_dump(mode='json'),
            'currency': model.currency, 'units': 'millions except per-share values',
            'valuation': valuation.model_dump(), 'sensitivity': matrix,
            'sensitivity_range': {'low': min(prices), 'high': max(prices)},
            'interpretation': 'This range measures sensitivity to specified assumptions; '
                              'it is not a confidence interval or a market-price forecast.',
            'warnings': warnings, 'assumptions': model.model_dump(mode='json')}
