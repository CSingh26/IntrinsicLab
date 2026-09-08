# IntrinsicLab design — 2026-09-08

## Financial question
How do operating performance, reinvestment, financing assumptions and terminal expectations change a defensible range of enterprise and equity values?

## Scope and design decisions
A stateless Python package calculates one explicit annual FCFF forecast, supports Gordon-growth and EV/EBITDA terminal methods, CAPM/WACC, comparable multiples and two-dimensional sensitivity. A FastAPI service serves its browser workbench as well as validated JSON endpoints. JSON assumption import/export carries source, as-of date, units and mode; an optional annual CSV normalizer accepts reported financial data with provenance. Scenario comparison is browser-local and explicitly labeled. No database or credentials are needed. No quote feed, LLM or automatic investment recommendation is justified for this tool.

Each layer has one responsibility: Pydantic contracts; normalization; pure numerical functions; application service; HTTP routing; presentation. Monetary inputs and outputs are in millions of one currency, shares are millions, per-share outputs are ordinary currency. Rates use decimal fractions in the API and displayed percentages in the UI. Annual fiscal periods and end-year discounting only.

## Financial / quantitative decisions
FCFF = EBIT - cash taxes + D&A - CapEx - change in operating NWC. Cash taxes = max(EBIT,0)×tax rate; no loss carryforward or immediate tax credit. NWC = revenue×NWC ratio and change is relative to opening NWC. D&A and CapEx ratios vary by forecast year. Forecast growth and reinvestment are transparent explicit assumptions.

Terminal growth must remain below WACC. Gordon perpetuity starts in year N+1 using normalized terminal EBIT and reinvestment: FCFF = NOPAT×(1-g/terminal ROIC); explicit terminal ROIC prevents pretending growth is costless. Terminal ROIC must be positive; stable EBIT must be positive; reinvestment fraction must be below one. Exit method multiplies final-year EBITDA. Show share of EV from terminal value, and flag heavy dependence.

EV bridge subtracts debt, preferred capital, and noncontrolling interests and adds nonoperating cash. Negative equity values are retained, not clamped. WACC uses market-value financing weights, cost of debt, and a constant tax-shield assumption. Invalid/negative comparison denominators return unavailable explanations rather than misleading ratios.

## Team responsibilities
Lead orchestrator: finance specification, mathematical conventions, data schema, engineering/UI and release. Independent reviewer to challenge finance, quant, engineering/security and recruiter presentation before release. Other project agents never edit this repository.

## UX
A research workbench with a assumptions sidebar, three decision-relevant outputs, explicit DEMO DATA badge, editable annual drivers, FCFF/discounted value charts, cash-flow bridge, WACC calculator, terminal sensitivity grid, peer comparison, source evidence and methodology. A user can import/export their own model, change scenarios, and inspect each annual calculation. Errors clear invalid/stale results. No fabricated provider fallback.

## Validation / release
Hand-computed financial identities and directional tests; malformed, nonfinite and bad-unit data; HTTP routes and import errors; browser user journey; lint/mypy/build. Incremental genuine commits and remote verification each milestone. GitHub Actions repeats checks. Independent review fixes precede release; >=15 meaningful development commits.
