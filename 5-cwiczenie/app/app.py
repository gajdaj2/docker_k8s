import os
import socket
import time

import redis
from flask import Flask, Response, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from logic import build_homepage, build_status_payload

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
APP_TITLE = os.getenv("APP_TITLE", "Testowanie i health checks")
START_TIME = time.time()
PAGE_VISITS = Counter("page_visits_total", "Liczba wejsc na strone glowna")


def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)


def get_uptime_seconds() -> int:
    return int(time.time() - START_TIME)


@app.route("/")
def home():
    retries = 5
    last_error = ""

    while retries > 0:
        try:
            client = get_redis_client()
            visits = client.incr("visits")
            PAGE_VISITS.inc()
            return build_homepage(APP_TITLE, visits)
        except Exception as error:
            last_error = str(error)
            retries -= 1
            time.sleep(1)

    payload = build_status_payload(False)
    payload["message"] = last_error
    return jsonify(payload), 500


@app.route("/health")
def health():
    try:
        client = get_redis_client()
        client.ping()
        visits_value = client.get("visits")
        payload = build_status_payload(True, int(visits_value) if visits_value else 0)
        payload["redis_host"] = REDIS_HOST
        payload["uptime_seconds"] = get_uptime_seconds()
        return jsonify(payload)
    except Exception as error:
        payload = build_status_payload(False)
        payload["message"] = str(error)
        payload["uptime_seconds"] = get_uptime_seconds()
        return jsonify(payload), 500


@app.route("/diag")
def diagnostics():
    payload = {
        "hostname": socket.gethostname(),
        "redis_host": REDIS_HOST,
        "uptime_seconds": get_uptime_seconds(),
    }
    return jsonify(payload)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
