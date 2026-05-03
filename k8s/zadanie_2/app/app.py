import os
import time

import redis
from flask import Flask

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
APP_TITLE = os.getenv("APP_TITLE", "Flask + Redis na Kubernetes")


def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


@app.route("/")
def home():
    retries = 5
    last_error = ""

    while retries > 0:
        try:
            client = get_redis_client()
            visits = client.incr("visits")
            return f"""
            <h1>{APP_TITLE}</h1>
            <p>Aplikacja Flask dziala w Kubernetes.</p>
            <p>Polaczenie z Redis dziala poprawnie.</p>
            <p><b>Liczba odwiedzin:</b> {visits}</p>
            """
        except Exception as error:
            last_error = str(error)
            retries -= 1
            time.sleep(1)

    return f"<h1>Blad polaczenia z Redis</h1><p>{last_error}</p>", 500


@app.route("/health")
def health():
    try:
        client = get_redis_client()
        client.ping()
        return {"status": "ok", "redis_host": REDIS_HOST}
    except Exception as error:
        return {"status": "error", "message": str(error)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
