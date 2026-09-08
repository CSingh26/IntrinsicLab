import pytest
from pydantic import ValidationError
from intrinsiclab.contracts import OperatingYear, Source, ValuationAssumptions


def test_rejects_nonfinite_and_misexpressed_rates():
    for value in [float('nan'), float('inf'), 25]:
        with pytest.raises(ValidationError):
            OperatingYear(growth=value)


def test_model_requires_positive_shares_and_source():
    with pytest.raises(ValidationError):
        ValuationAssumptions(shares=0)
    with pytest.raises(ValidationError):
        Source(provider='')


def test_unknown_keys_fail_instead_of_silently_changing_assumptions():
    with pytest.raises(ValidationError):
        OperatingYear(growth=0.05, margni=0.2)


def test_forecast_limit_and_currency_units():
    with pytest.raises(ValidationError):
        ValuationAssumptions(years=[])
    with pytest.raises(ValidationError):
        ValuationAssumptions(currency='usd')
