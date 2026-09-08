# Valuation methodology

All forecasts are annual and use end-of-year discounting. Rates are decimal fractions. Money and shares use millions of the same currency so their ratio is ordinary currency per share. Enterprise cash flows are discounted at WACC; equity cash flows would require a different discount rate and are out of scope.

## Operating cash flows
Revenue_t = Revenue_(t-1) × (1+growth_t). EBIT = revenue×operating margin. NOPAT = EBIT - max(EBIT,0)×tax rate. FCFF = NOPAT + D&A - CapEx - Δoperating net working capital. NWC is non-cash operating working capital, excluding financing items. Opening NWC is an explicit balance, not silently assumed to be zero. Negative EBIT does not generate an immediate tax cash inflow; loss carryforwards are not modeled.

## Opportunity cost and terminal value
CAPM cost of equity = risk-free rate + beta×equity risk premium. WACC = E/(D+E)×Re + D/(D+E)×Rd×(1-T), where E and D are market values. A usable tax shield is assumed. Net debt must not replace gross debt in these weights.

For Gordon growth, terminal-year revenue = final forecast revenue×(1+g), terminal NOPAT = revenue×terminal margin×(1-T), terminal reinvestment = NOPAT×g/ROIC, and terminal FCFF = NOPAT - reinvestment. Terminal value = terminal FCFF/(WACC-g), requiring WACC>g. Terminal ROIC makes the reinvestment cost of growth explicit. For contraction, negative reinvestment represents disinvestment and is a strong assumption.

For exit multiples, terminal value = final explicit-year EBITDA×EV/EBITDA multiple. This combines intrinsic forecasting with a relative-pricing assumption, not an independent confirmation of value.

EV = Σ FCFF_t/(1+WACC)^t + terminal value/(1+WACC)^N. Equity value = EV - debt - preferred equity - noncontrolling interests + nonoperating cash. Per-share value = equity value/diluted shares. A negative equity residual is displayed as a model diagnostic, not an executable negative market price.

## Primary references
- [Damodaran, valuation lectures](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/lectures/val.html): matching cash flows and discount rates.
- [Damodaran, terminal value approaches](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/termvalapproaches.htm): closure, stable growth and economic constraints.
- [CFA Institute, Free Cash Flow Valuation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/free-cash-flow-valuation): FCFF versus FCFE.

No current market estimates are copied from these references. Every model parameter is an explicitly labeled user or demo assumption.
