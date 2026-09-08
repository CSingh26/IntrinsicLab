import pytest
from intrinsiclab.ingest import normalize_annual_csv
from intrinsiclab.contracts import Source

SOURCE = Source(provider='Uploaded filing', as_of='2026-09-08', mode='USER INPUT')
CSV = 'fiscal_year,currency,revenue,ebit,da,capex,nwc\n2024,USD,100,20,3,5,10\n2025,USD,110,22,3,6,11\n'


def test_preserves_units_source_and_annual_growth():
    result = normalize_annual_csv(CSV, SOURCE)
    assert result['rows'][1]['revenue_growth'] == pytest.approx(0.1)
    assert result['units'] == 'millions'
    assert result['source']['provider'] == 'Uploaded filing'


@pytest.mark.parametrize('bad', [CSV.replace('2025','2024'), CSV.replace('2025','2027'), CSV.replace('110','NaN'), CSV.replace('2025,USD','2025,EUR'), CSV.replace('ebit','EBIT')])
def test_rejects_duplicate_missing_nonfinite_or_inconsistent_data(bad):
    with pytest.raises(ValueError):
        normalize_annual_csv(bad, SOURCE)
