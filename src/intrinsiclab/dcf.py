"""DCF with explicit terminal reinvestment and an auditable enterprise/equity bridge."""
from intrinsiclab.contracts import Contract, Finite, ValuationAssumptions
from intrinsiclab.forecast import CashFlowYear, project_cash_flows


class Valuation(Contract):
    forecast: list[CashFlowYear]
    discounted_fcff: list[Finite]
    terminal_fcff: Finite | None
    terminal_value: Finite
    discounted_terminal_value: Finite
    enterprise_value: Finite
    net_claims: Finite
    equity_value: Finite
    price_per_share: Finite
    terminal_share_of_ev: Finite | None


def value_company(model: ValuationAssumptions) -> Valuation:
    forecast = project_cash_flows(model)
    terminal_fcff: float | None = None
    if model.terminal_method == 'exit_multiple':
        if forecast[-1].ebitda <= 0:
            raise ValueError('Exit multiple requires positive final-year EBITDA')
        terminal_value = forecast[-1].ebitda * model.exit_multiple
    else:
        if model.terminal_growth >= model.wacc:
            raise ValueError('Terminal growth must be below WACC')
        reinvestment_rate = model.terminal_growth / model.terminal_roic
        if reinvestment_rate >= 1:
            raise ValueError('Terminal ROIC must exceed positive terminal growth')
        # Growth requires reinvestment; ROIC translates growth into a cash requirement.
        terminal_nopat = (forecast[-1].revenue * (1 + model.terminal_growth)
                          * model.terminal_margin * (1 - model.tax_rate))
        terminal_fcff = terminal_nopat * (1 - reinvestment_rate)
        terminal_value = terminal_fcff / (model.wacc - model.terminal_growth)
    discounted = [row.fcff / (1 + model.wacc) ** (i + 1) for i, row in enumerate(forecast)]
    discounted_terminal = terminal_value / (1 + model.wacc) ** len(forecast)
    enterprise = sum(discounted) + discounted_terminal
    # Enterprise value belongs to all capital claimants. Cash is added only if nonoperating.
    net_claims = model.debt + model.preferred_equity + model.noncontrolling_interests - model.cash
    equity = enterprise - net_claims
    return Valuation(forecast=forecast, discounted_fcff=discounted, terminal_fcff=terminal_fcff,
                     terminal_value=terminal_value, discounted_terminal_value=discounted_terminal,
                     enterprise_value=enterprise, net_claims=net_claims, equity_value=equity,
                     price_per_share=equity / model.shares,
                     terminal_share_of_ev=discounted_terminal / enterprise if enterprise > 0 else None)
