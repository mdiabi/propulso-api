from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

@pytest.mark.parametrize("visitor_id", ["1", "2"])  # Parameterize the test cases
def test_store_visitor_visits(visitor_id):
    response = client.get(f"/store/1/visitor/{visitor_id}/visits")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_store_visitors():
    response = client.get("/store/1/visitors")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_store_statistics():
    date = "2023-06-09"
    response = client.get(f"/store/1/statistics/{date}")
    assert response.status_code == 200
    assert "average_time_visit" in response.json()
    assert "total_daily_visits" in response.json()
    assert "total_daily_visitors" in response.json()
