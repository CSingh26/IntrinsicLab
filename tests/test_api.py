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
