# Data dictionary

| Field | Meaning | Units / convention |
|---|---|---|
| revenue | Opening annual sales | Currency millions, positive |
| opening_nwc | Noncash operating current assets less operating current liabilities | Currency millions; may be negative |
| growth | Revenue growth from previous annual period | Decimal fraction > -1 |
| operating_margin | EBIT / revenue | Decimal fraction |
| da_ratio / capex_ratio | Depreciation/amortization or capital expenditures / revenue | Nonnegative fractions; CapEx is cash outflow |
| nwc_ratio | Operating NWC / revenue | Decimal fraction; excludes cash/debt |
| tax_rate | Cash tax rate on positive operating earnings | Decimal fraction; no NOL tracking |
| wacc | Nominal annual weighted cost of financing | Decimal fraction; same currency as cash flows |
| terminal_growth | Indefinite nominal growth | Less than WACC and terminal ROIC |
| terminal_roic | Stable return on incremental invested capital | Positive fraction; drives reinvestment |
| terminal_margin | Stable EBIT / sales | Positive fraction |
| exit_multiple | EV / final explicit-year EBITDA | Positive multiplier |
| debt | All debt claims at valuation date | Currency millions; use market value where available |
| cash | Excess / nonoperating cash to add to EV | Currency millions; avoid adding operating cash twice |
| preferred_equity / noncontrolling_interests | Additional enterprise claims | Currency millions |
| shares | Current diluted shares used in equity allocation | Millions |
| price_per_share | Residual equity value / diluted shares | Ordinary currency per share |
| source | Provider, as-of date, source mode, reference and transformation | Required; DEMO DATA or USER INPUT |

Annual CSV requires exactly `fiscal_year,currency,revenue,ebit,da,capex,nwc`. All rows use one currency and consecutive ascending fiscal years. Fiscal-year labels do not resolve 52/53-week distortions: the analyst must judge comparability. Quarterly figures are not annualized silently. No split/dividend/FX normalization is attempted.

Comparable JSON requires `source` and `peers`; each peer has company/currency/price/shares/debt/cash/revenue/ebitda/net_income/book_equity, with optional preferred_equity/noncontrolling_interests. Use consistent trailing annual periods and contemporaneous prices and shares. Every value is user supplied; the tool has no live quote feed.
