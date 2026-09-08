"""Stateless local research API. Calculations never request external provider data."""
import json
from importlib.resources import files
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import Field

from intrinsiclab.capital import cost_of_capital
from intrinsiclab.comparables import Comparable, trading_multiples
from intrinsiclab.contracts import CapitalStructure, Contract, Source, ValuationAssumptions
from intrinsiclab.http_limits import BodyLimitMiddleware
from intrinsiclab.ingest import normalize_annual_csv
from intrinsiclab.service import analyze

app = FastAPI(title='IntrinsicLab', version='1.0.0')
app.add_middleware(BodyLimitMiddleware)


class StatementImport(Contract):
    content: str = Field(max_length=250_000)
    source: Source


class PeerImport(Contract):
    peers: list[Comparable] = Field(min_length=1, max_length=100)
    source: Source


@app.exception_handler(ValueError)
async def economic_error(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse({'detail': str(exc)}, status_code=422)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    # Exclude raw inputs: nonfinite input cannot be serialized as strict JSON.
    errors = [{'location': list(e['loc']), 'message': e['msg']} for e in exc.errors()]
    return JSONResponse({'detail': errors}, status_code=422)


@app.get('/api/health')
def health() -> dict[str, str]:
    return {'status': 'ok', 'engine_version': '1.0.0'}


@app.get('/api/demo')
def demo() -> dict[str, Any]:
    result: dict[str, Any] = json.loads(files('intrinsiclab').joinpath('data/demo.json').read_text())
    return result


@app.post('/api/valuations')
def valuations(model: ValuationAssumptions) -> dict[str, Any]:
    return analyze(model)


@app.post('/api/cost-of-capital')
def capital(model: CapitalStructure) -> dict[str, float]:
    return cost_of_capital(model)


@app.post('/api/statements/normalize')
def normalize(payload: StatementImport) -> dict[str, Any]:
    return normalize_annual_csv(payload.content, payload.source)


@app.post('/api/comparables')
def comparables(payload: PeerImport) -> dict[str, Any]:
    if len({peer.currency for peer in payload.peers}) > 1:
        raise ValueError('Normalize peer financials to one currency before comparison')
    return {'peers': [trading_multiples(peer) for peer in payload.peers],
            'source': payload.source.model_dump(mode='json')}

# The installed wheel contains the same browser assets used during development.
from pathlib import Path  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402

STATIC_DIR = Path(__file__).parent / 'static'
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


@app.get('/', include_in_schema=False)
def workbench() -> FileResponse:
    return FileResponse(STATIC_DIR / 'index.html')
