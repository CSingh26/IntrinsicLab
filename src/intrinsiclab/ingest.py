"""Strict annual CSV ingestion, without guessing missing financial observations."""
import csv
import io
from typing import Any

from pydantic import Field

from intrinsiclab.contracts import Contract, Finite, Nonnegative, Positive, Source


class AnnualRow(Contract):
    fiscal_year: int = Field(ge=1900, le=2100)
    currency: str = Field(pattern=r'^[A-Z]{3}$')
    revenue: Positive
    ebit: Finite
    da: Nonnegative
    capex: Nonnegative
    nwc: Finite


def normalize_annual_csv(content: str, source: Source) -> dict[str, Any]:
    """Rows contain millions; fiscal periods must be consecutive and in input order."""
    if len(content.encode()) > 250_000:
        raise ValueError('CSV exceeds 250 KB limit')
    reader = csv.DictReader(io.StringIO(content))
    required = list(AnnualRow.model_fields)
    if reader.fieldnames is None or sorted(reader.fieldnames) != sorted(required):
        raise ValueError('Required columns: ' + ','.join(required))
    rows = [AnnualRow.model_validate(row) for row in reader]
    if not 1 <= len(rows) <= 100:
        raise ValueError('Provide 1 to 100 annual rows')
    result = []
    previous: AnnualRow | None = None
    for row in rows:
        if row.currency != rows[0].currency:
            raise ValueError('All annual amounts must use the same currency')
        if previous and row.fiscal_year != previous.fiscal_year + 1:
            raise ValueError('Fiscal years must be unique, ordered and consecutive')
        result.append({**row.model_dump(),
                       'revenue_growth': row.revenue / previous.revenue - 1 if previous else None,
                       'operating_margin': row.ebit / row.revenue,
                       'da_ratio': row.da / row.revenue,
                       'capex_ratio': row.capex / row.revenue,
                       'nwc_ratio': row.nwc / row.revenue})
        previous = row
    return {'rows': result, 'units': 'millions', 'frequency': 'annual',
            'currency': rows[0].currency, 'source': source.model_dump(mode='json')}
