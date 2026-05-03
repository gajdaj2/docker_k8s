import os

import requests


APP_BASE_URL = os.getenv("APP_BASE_URL", "http://flask-service-zad3")


def test_health_endpoint_reports_redis_connection():
    response = requests.get(f"{APP_BASE_URL}/health", timeout=5)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["redis_host"] == "redis-service-zad3"


def test_homepage_is_available():
    response = requests.get(f"{APP_BASE_URL}/", timeout=5)

    assert response.status_code == 200
    assert "Liczba odwiedzin" in response.text
    assert "Polaczenie z Redis dziala poprawnie." in response.text
