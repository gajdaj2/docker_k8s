# Copilot instructions

## Repository shape

- This repository is a Docker/Kubernetes training workspace made of **standalone exercises**, not one integrated application.
- Work from the relevant subdirectory (`1-cwiczenie`, `2-cwiczenia`, `3-cwiczenie`, `projekt-compose`) instead of assuming repo-root commands.
- The root `main.py` is a PyCharm sample file and is usually unrelated to the exercises.
- Existing READMEs and learner-facing examples are in **Polish**; keep new docs and visible app text aligned unless asked to switch language.

## Build, run, and verification commands

| Area | Commands |
| --- | --- |
| `1-cwiczenie` | `cd 1-cwiczenie && npm start`<br>`cd 1-cwiczenie && docker build -t node-basic . && docker run --rm -p 3000:3000 node-basic` |
| `2-cwiczenia` | `cd 2-cwiczenia && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python app.py`<br>`cd 2-cwiczenia && docker build -t flask-students-app . && docker run --rm -p 5000:5000 flask-students-app`<br>Manual endpoint checks: `curl http://localhost:5000/` and `curl http://localhost:5000/health` |
| `3-cwiczenie` | `cd 3-cwiczenie && docker build -t fastapi-basic .`<br>`cd 3-cwiczenie && docker build -f Dockerfile_z_multistage -t fastapi-multistage .`<br>`cd 3-cwiczenie && docker run --rm -p 8000:8000 fastapi-basic`<br>`cd 3-cwiczenie && docker run --rm -p 8000:8000 fastapi-multistage`<br>Manual endpoint check: `curl http://localhost:8000/health` |
| `projekt-compose` | `cd projekt-compose && docker compose up --build`<br>`cd projekt-compose && docker compose ps`<br>`cd projekt-compose && docker compose logs`<br>`cd projekt-compose && docker compose logs web`<br>`cd projekt-compose && docker compose logs db`<br>`cd projekt-compose && docker compose exec db psql -U appuser -d appdb`<br>`cd projekt-compose && docker compose down` or `docker compose down -v`<br>Manual check: `curl http://localhost:8000/` |

There is currently **no automated test suite or lint configuration** in the repository. Do not assume `pytest`, `npm test`, or lint commands exist unless you add them intentionally.

## High-level architecture

- `1-cwiczenie` is the simplest example: a single-file Node HTTP server in `app.js`, packaged with a basic Dockerfile and started via `npm start`.
- `2-cwiczenia` is a single-service Flask example. `app.py` exposes `/` and `/health`, `requirements.txt` pins Flask, and the Dockerfile runs the app directly with `python app.py`.
- `3-cwiczenie` is a FastAPI exercise organized as a Python package under `app/`. The important design point is the comparison between two image builds: `Dockerfile` and `Dockerfile_z_multistage` should stay functionally equivalent while differing only in dependency installation strategy.
- `projekt-compose` is the only multi-service setup. `docker-compose.yml` defines `web` and `db`; `web/app.py` reads connection details from environment variables, connects to PostgreSQL using the Compose service name `db`, retries connection on startup, and relies on the named volume `pgdata` for database persistence.

## Key conventions

- Treat each exercise directory as self-contained: dependencies, ports, Docker context, and commands are local to that folder.
- Preserve the current port mapping conventions: `3000` for `1-cwiczenie`, `5000` for `2-cwiczenia`, and `8000` for both `3-cwiczenie` and `projekt-compose`.
- In `projekt-compose`, keep database configuration synchronized between `docker-compose.yml` and `web/app.py` defaults (`DB_HOST=db`, `DB_NAME=appdb`, `DB_USER=appuser`, `DB_PASSWORD=secret`).
- In `projekt-compose`, do not replace the retry loop in `web/app.py` with a simple one-shot connection; it exists because `depends_on` does not guarantee database readiness.
- In `3-cwiczenie`, update both Dockerfiles together when changing app startup, copied files, or dependency handling so the classic and multistage builds stay comparable.
