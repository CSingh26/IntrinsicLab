import pytest
from intrinsiclab.contracts import ValuationAssumptions


@pytest.fixture
def assumptions():
    return ValuationAssumptions(company='Example Co', currency='USD', source={'provider':'Synthetic educational fixture','as_of':'2026-09-08','mode':'DEMO DATA'}, base_year=2025, revenue=100, opening_nwc=10, years=[{'growth':.1,'operating_margin':.2,'da_ratio':.03,'capex_ratio':.05,'nwc_ratio':.1}], tax_rate=.25,wacc=.1,terminal_growth=.02,terminal_margin=.2,terminal_roic=.1,debt=20,cash=5,shares=10)
