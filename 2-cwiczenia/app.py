from flask import Flask

app = Flask(__name__)


@app.get("/")
def home() -> str:
    return "Czesc! To jest aplikacja Flask uruchomiona w Dockerze.\n"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

