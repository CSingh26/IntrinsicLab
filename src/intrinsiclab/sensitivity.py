"""Recalculate each cell, retaining invalid economic regions as unavailable."""
from typing import Any
from intrinsiclab.contracts import ValuationAssumptions
from intrinsiclab.dcf import value_company


def sensitivity_matrix(model: ValuationAssumptions, waccs: list[float],
                       terminal_values: list[float]) -> dict[str, Any]:
    if not 1 <= len(waccs) <= 15 or not 1 <= len(terminal_values) <= 15:
        raise ValueError('Sensitivity axes require 1 to 15 values each')
    key = 'terminal_growth' if model.terminal_method == 'gordon' else 'exit_multiple'
    rows = []
    for wacc in waccs:
        cells: list[dict[str, Any]] = []
        for terminal in terminal_values:
            try:
                candidate = ValuationAssumptions.model_validate(
                    model.model_dump() | {'wacc': wacc, key: terminal})
                price = value_company(candidate).price_per_share
                cells.append({'price': price, 'reason': None})
            except ValueError as exc:
                cells.append({'price': None, 'reason': str(exc)})
        rows.append({'wacc': wacc, 'values': cells})
    return {'axis': key, 'columns': terminal_values, 'rows': rows,
            'units': model.currency + ' per share'}
