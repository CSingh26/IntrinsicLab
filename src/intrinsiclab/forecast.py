"""Annual unlevered cash flows from explicit operating and reinvestment assumptions."""
from intrinsiclab.contracts import Contract, Finite, ValuationAssumptions


class CashFlowYear(Contract):
    year: int
    revenue: Finite
    ebit: Finite
    cash_taxes: Finite
    nopat: Finite
    da: Finite
    ebitda: Finite
    capex: Finite
    nwc: Finite
    change_nwc: Finite
    fcff: Finite


def project_cash_flows(model: ValuationAssumptions) -> list[CashFlowYear]:
    revenue, prior_nwc = model.revenue, model.opening_nwc
    rows = []
    for index, year in enumerate(model.years, start=1):
        revenue *= 1 + year.growth
        ebit = revenue * year.operating_margin
        cash_taxes = max(ebit, 0) * model.tax_rate
        nopat = ebit - cash_taxes
        da, capex, nwc = revenue * year.da_ratio, revenue * year.capex_ratio, revenue * year.nwc_ratio
        change_nwc = nwc - prior_nwc
        # Reinvestment consumes cash even when depreciation lowers reported earnings.
        fcff = nopat + da - capex - change_nwc
        rows.append(CashFlowYear(year=model.base_year + index, revenue=revenue, ebit=ebit,
                                 cash_taxes=cash_taxes, nopat=nopat, da=da, ebitda=ebit + da,
                                 capex=capex, nwc=nwc, change_nwc=change_nwc, fcff=fcff))
        prior_nwc = nwc
    return rows
