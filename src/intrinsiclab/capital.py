"""Financing opportunity cost using market-value weights."""
from intrinsiclab.contracts import CapitalStructure


def cost_of_capital(capital: CapitalStructure) -> dict[str, float]:
    total = capital.equity_market_value + capital.debt_market_value
    if total <= 0:
        raise ValueError('Positive market-value financing is required')
    equity_weight = capital.equity_market_value / total
    cost_of_equity = capital.risk_free_rate + capital.beta * capital.equity_risk_premium
    # WACC blends investor opportunity costs; debt's tax shield assumes taxable capacity.
    after_tax_debt = capital.pretax_cost_of_debt * (1 - capital.tax_rate)
    return {'cost_of_equity': cost_of_equity, 'equity_weight': equity_weight,
            'debt_weight': 1 - equity_weight, 'after_tax_cost_of_debt': after_tax_debt,
            'wacc': equity_weight * cost_of_equity + (1 - equity_weight) * after_tax_debt}
