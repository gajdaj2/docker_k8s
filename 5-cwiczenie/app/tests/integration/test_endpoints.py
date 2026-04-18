import os

import requests


APP_BASE_URL = os.getenv("APP_BASE_URL", "http://app:5000")


def test_health_endpoint_reports_redis_connection():
    response = requests.get(f"{APP_BASE_URL}/health", timeout=5)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["redis"] == "connected"


def test_homepage_increases_visits_counter():
    first = requests.get(f"{APP_BASE_URL}/", timeout=5)
    second = requests.get(f"{APP_BASE_URL}/", timeout=5)

    assert first.status_code == 200
    assert second.status_code == 200
    assert "Liczba odwiedzin" in second.text


def test_metrics_endpoint_is_exposed():
    response = requests.get(f"{APP_BASE_URL}/metrics", timeout=5)

    assert response.status_code == 200
    assert "page_visits_total" in response.text
