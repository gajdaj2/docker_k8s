import requests


def test_healthcheck():
    response = requests.get("http://localhost:8080/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


