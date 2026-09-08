# Contributing

Start financial changes with a hand-worked example and state units, timing, signs and economic assumptions. Add a failing behavior test, implement the financial rule in its domain module, and run `scripts/verify.sh`. Never duplicate formulas in browser components. Include provenance for external data; fictional fixtures must say DEMO DATA. Keep model errors visible and document methodology changes. Do not commit credentials, private borrower/company data or `.env` files.

Public deployment is a separate design decision: authentication, rate limits and transport security must be designed for that environment. The supplied server binds to loopback for personal research.
