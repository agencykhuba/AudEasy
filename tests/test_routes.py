import pytest
from app.app import app
from sqlalchemy.exc import OperationalError

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"AudEasy" in response.data

def test_health(client):
    response = client.get("/health")
    assert response.status_code in [200, 503]

def test_health_db_failure(client, monkeypatch):
    def mock_connect(*args, **kwargs):
        raise OperationalError("mock", "mock", "DB connection failed")
    monkeypatch.setattr("sqlalchemy.create_engine", lambda *args, **kwargs: type('MockEngine', (), {'connect': mock_connect})())
    response = client.get("/health")
    assert response.status_code == 503
    assert b"failed" in response.data

def test_audit(client):
    response = client.get("/audit")
    assert response.status_code == 200
    assert b"Customer Delight" in response.data

def test_404_route(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
