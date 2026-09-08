from fastapi.testclient import TestClient
from intrinsiclab.api import app

client = TestClient(app)


def test_full_demo_to_valuation_journey():
    data = client.get('/api/demo').json()
    response = client.post('/api/valuations', json=data)
    assert response.status_code == 200
    result = response.json()
    assert result['source']['mode'] == 'DEMO DATA'
    assert len(result['valuation']['forecast']) == 5
    assert len(result['sensitivity']['rows']) == 5


def test_invalid_assumptions_fail_without_substituting_data(assumptions):
    body = assumptions.model_dump(mode='json') | {'shares': 0}
    assert client.post('/api/valuations', json=body).status_code == 422
    body = assumptions.model_dump(mode='json') | {'terminal_growth': .1}
    result = client.post('/api/valuations', json=body)
    assert result.status_code == 422
    assert 'below WACC' in result.json()['detail']


def test_capital_and_import_routes(assumptions):
    assert client.get('/api/health').json() == {'status':'ok','engine_version':'1.0.0'}
    result = client.post('/api/statements/normalize', json={'content':'bad', 'source':assumptions.source.model_dump(mode='json')})
    assert result.status_code == 422


def test_request_size_limit():
    result = client.post('/api/valuations', content='x' * 600_000)
    assert result.status_code == 413


def test_workbench_is_served_with_functional_assets():
    response = client.get('/')
    assert response.status_code == 200
    assert 'IntrinsicLab' in response.text
    assert 'id="valuation-form"' in response.text
    assert client.get('/static/app.js').status_code == 200
    assert client.get('/static/styles.css').status_code == 200


def test_nonfinite_and_unknown_inputs_do_not_escape_validation(assumptions):
    import json
    body=assumptions.model_dump(mode='json') | {'revenue':float('nan')}
    response=client.post('/api/valuations', content=json.dumps(body), headers={'Content-Type':'application/json'})
    assert response.status_code == 422
    assert 'Input should be a finite number' in response.text
    assert 'NaN' not in response.text


def test_inconsistent_peer_currency_returns_error(assumptions):
    peer=dict(company='Example',currency='USD',price=20,shares=10,debt=10,cash=2,revenue=20,ebitda=2,net_income=1,book_equity=5)
    response=client.post('/api/comparables',json={'peers':[peer,peer|{'currency':'EUR'}],'source':assumptions.source.model_dump(mode='json')})
    assert response.status_code == 422


def test_extremely_small_peer_denominator_remains_unavailable(assumptions):
    peer=dict(company='Example',currency='USD',price=20,shares=10,debt=10,cash=2,
              revenue=20,ebitda=1e-310,net_income=1e-310,book_equity=5)
    response=client.post('/api/comparables',json={'peers':[peer], 'source':assumptions.source.model_dump(mode='json')})
    assert response.status_code == 200
    assert response.json()['peers'][0]['pe']['value'] is None
    assert response.json()['peers'][0]['ev_ebitda']['value'] is None
    assert 'finite' in response.json()['peers'][0]['pe']['reason'].lower()
