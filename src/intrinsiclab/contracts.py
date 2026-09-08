"""Single-currency annual contracts. Rates are fractions; money/shares are millions."""
from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

Finite = Annotated[float, Field(allow_inf_nan=False)]
Positive = Annotated[Finite, Field(gt=0, le=1e12)]
Nonnegative = Annotated[Finite, Field(ge=0, le=1e12)]
Fraction = Annotated[Finite, Field(ge=0, le=1)]


class Contract(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Source(Contract):
    provider: str = Field(min_length=1, max_length=200)
    as_of: date
    mode: Literal['DEMO DATA', 'USER INPUT']
    reference: str = Field(default='', max_length=2000)
    retrieved_at: str | None = Field(default=None, max_length=100)
    transformation: str = Field(default='User-specified annual valuation assumptions', max_length=500)


class OperatingYear(Contract):
    growth: Annotated[Finite, Field(gt=-1, le=2)] = 0.05
    operating_margin: Annotated[Finite, Field(ge=-1, le=1)] = 0.2
    da_ratio: Fraction = 0.03
    capex_ratio: Fraction = 0.05
    nwc_ratio: Annotated[Finite, Field(ge=-1, le=1)] = 0.1


class CapitalStructure(Contract):
    equity_market_value: Nonnegative
    debt_market_value: Nonnegative
    risk_free_rate: Annotated[Finite, Field(ge=-0.1, le=0.5)]
    beta: Annotated[Finite, Field(ge=-5, le=5)]
    equity_risk_premium: Annotated[Finite, Field(ge=0, le=0.5)]
    pretax_cost_of_debt: Annotated[Finite, Field(ge=0, le=0.5)]
    tax_rate: Fraction


class ValuationAssumptions(Contract):
    company: str = Field(min_length=1, max_length=120)
    currency: str = Field(pattern=r'^[A-Z]{3}$')
    source: Source
    base_year: int = Field(ge=1900, le=2100)
    revenue: Positive
    opening_nwc: Annotated[Finite, Field(ge=-1e12, le=1e12)]
    years: list[OperatingYear] = Field(min_length=1, max_length=15)
    tax_rate: Fraction
    wacc: Annotated[Finite, Field(gt=0, le=0.5)]
    terminal_method: Literal['gordon', 'exit_multiple'] = 'gordon'
    terminal_growth: Annotated[Finite, Field(gt=-0.1, le=0.15)] = 0.025
    terminal_margin: Annotated[Finite, Field(gt=0, le=1)] = 0.2
    terminal_roic: Annotated[Finite, Field(gt=0, le=1)] = 0.15
    exit_multiple: Annotated[Finite, Field(gt=0, le=100)] = 10
    debt: Nonnegative
    cash: Nonnegative
    preferred_equity: Nonnegative = 0
    noncontrolling_interests: Nonnegative = 0
    shares: Positive
