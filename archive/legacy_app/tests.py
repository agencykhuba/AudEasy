import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_login_success(client):
    response = client.post('/login', json={'email': 'test@audeasy.com', 'password': 'pass123'})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert 'user_id' in response.json
    assert 'role' in response.json

def test_login_failure(client):
    response = client.post('/login', json={'email': 'test@audeasy.com', 'password': 'wrong'})
    assert response.status_code == 401
    assert response.json['status'] == 'error'
    assert 'user_id' not in response.json
    assert 'role' not in response.json
    assert response.json['message'] == 'Invalid credentials'

def test_audit_submission_success(client):
    response = client.post('/audit', json={
        'store_id': '123e4567-e89b-12d3-a456-426614174000',
        'auditor_id': '123e4567-e89b-12d3-a456-426614174001',
        'template_id': '123e4567-e89b-12d3-a456-426614174002',
        'visit_datetime': '2025-09-13T09:00:00Z'
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert 'visit_id' in response.json

def test_audit_submission_missing_data(client):
    response = client.post('/audit', json={'store_id': '123e4567-e89b-12d3-a456-426614174000'})
    assert response.status_code == 500
    assert response.json['status'] == 'error'
    assert 'message' in response.json