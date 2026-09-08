# IntrinsicLab portfolio delivery

Repository: https://github.com/CSingh26/IntrinsicLab (public).
Primary question: how do operating economics, reinvestment and opportunity cost determine a valuation range?
CS: typed modular domain design, bounded HTTP inputs, reproducible pure functions, JSON/CSV ingestion, interactive browser state, regression tests and CI.
Finance: FCFF, NOPAT, capital efficiency, CAPM/WACC, Gordon and exit-multiple terminal values, equity claims and comparable multiples.

## Observed verification
- `pytest -q`:34 passing financial/data/API tests at59906f6.
- `npm run test:browser`:5 passing journeys, including currency consistency and stale financing regressions.
- `ruff check src tests`, `mypy src`, `npm run check`:pass.
- `python -m build`:wheel and source distribution built successfully; same static assets ship in wheel.
- Tracked text secret-pattern scan:pass. This heuristic check is not a comprehensive security audit.
- GitHub Actions run34278837069 at5755df9:success. Latest fix59906f6 queued for repeat verification when this report was written; final portfolio audit records its result directly from GitHub.
- Independent reviewer: CreditLens lead examined finance, quant, API/security and UX. Two P2 findings reproduced and fixed in59906f6: mixed-currency partial import and stale Apply WACC state. Scoped re-review requested.
-17 meaningful commits through59906f6, each representing actual incremental development. No empty or artificial history commits.

## Scope and limitations
Core workbench accepts real user inputs and explicit fictional demo data, performs real calculations and exports reproducible evidence. No external data provider credentials are needed. The model is annual, nominal, single-currency, and assumes constant taxes with no loss carryforward. Terminal economics and equity claims require analyst judgment. It is a local research tool, not a publicly deployed multi-user service. Detailed limitations are in docs/LIMITATIONS.md.

The exact latest SHA, CI result and clean/remote status are independently audited in the master portfolio report; report commits naturally follow the implementation SHA.
