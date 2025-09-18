from app.app import app

def test_root():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"AudEasy" in response.data

def test_health():
    with app.test_client() as client:
        response = client.get("/health")
        assert response.status_code in [200, 503]

def test_audit():
    with app.test_client() as client:
        response = client.get("/audit")
        assert response.status_code == 200
        assert b"Customer Delight" in response.data
