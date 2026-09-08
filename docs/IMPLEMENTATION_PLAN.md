# IntrinsicLab implementation plan

Goal: an assumption-driven valuation workbench with auditable calculation evidence.
Architecture: typed data → normalization → pure finance engines → service/API → browser UI.
Spec: docs/DESIGN.md. Tests precede each financial behavior; commands below run in .venv.

Each numbered task is one independent milestone and commit; actual code is developed only as its preceding task and tests are verified, never split retrospectively.

1. Initialize installable Python package, license, ignored environment and reproducible dependencies; validate import/build.
2. Record specification, methodology and source references. Review financial units and terminal reinvestment consistency.
3. Create contracts.py with Source, OperatingYear, CapitalStructure and ValuationAssumptions; test finite values, invalid rates, positive shares and forecast bounds.
4. Add ingest.py annual CSV normalization with source metadata; test duplicates, annual cadence, missing/unknown columns, inconsistent currency and malformed values.
5. Add capital.py CAPM and market-value WACC; test 80/20 funding example, no funding and nonfinite errors.
6. Add forecast.py annual revenue/EBIT/NOPAT/D&A/CapEx/NWC/FCFF schedule; test accounting bridge, loss tax handling and opening NWC.
7. Add dcf.py Gordon terminal and EV/equity bridge; test hand-calculated perpetuity, g>=WACC, negative equity.
8. Extend dcf.py exit multiple method; test final-year EBITDA basis and discount timing.
9. Add comparables.py P/E, EV/EBITDA, EV/sales, P/B; test economic denominators and debt/cash bridge.
10. Add sensitivity.py WACC×growth or exit-multiple matrix and service.py interpretation; test monotonic discount-rate effects and unavailable cells.
11. Expose validated FastAPI calculation, normalization and demo routes; test schema/error metadata and strict JSON outputs.
12. Build functional browser workflow for annual drivers, source, WACC, imports and outputs; check requests and error clearing.
13. Add interactive projections, bridge and sensitivity visualizations with units/tooltips and accessible tabular alternatives.
14. Add scenario comparison and downloadable reproducible evidence with deterministic IDs; test consistent imported assumptions.
15. Expand independent financial/HTTP and smoke/edge regression coverage; run full lint/typecheck/tests/build.
16. Document finance story, concrete observed demo calculation, model limits, data dictionary, architecture, contributing and reproducible commands; capture actual UI.
17. Add security/CI release verification, review fixes, confirm >=15 meaningful commits and remote latest SHA/CI before final release report.
