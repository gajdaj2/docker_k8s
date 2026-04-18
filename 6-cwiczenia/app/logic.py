def build_status_payload(redis_ok: bool, visits: int | None = None) -> dict:
    return {
        "status": "ok" if redis_ok else "error",
        "redis": "connected" if redis_ok else "disconnected",
        "visits": visits,
    }


def build_homepage(title: str, visits: int) -> str:
    return f"""
    <h1>{title}</h1>
    <p>Aplikacja dziala w kontenerze Docker.</p>
    <p>Redis jest dostepny z poziomu kontenera aplikacji.</p>
    <p><b>Liczba odwiedzin:</b> {visits}</p>
    """
