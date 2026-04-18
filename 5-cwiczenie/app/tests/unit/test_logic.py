from logic import build_homepage, build_status_payload


def test_build_status_payload_returns_ok():
    payload = build_status_payload(True, 3)

    assert payload == {
        "status": "ok",
        "redis": "connected",
        "visits": 3,
    }


def test_build_status_payload_returns_error():
    payload = build_status_payload(False)

    assert payload["status"] == "error"
    assert payload["redis"] == "disconnected"
    assert payload["visits"] is None


def test_build_homepage_contains_title_and_visits():
    html = build_homepage("Modul testowy", 7)

    assert "Modul testowy" in html
    assert "Liczba odwiedzin" in html
    assert "7" in html
