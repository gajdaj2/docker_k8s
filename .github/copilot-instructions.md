# Copilot instructions

## Repository shape

- This repository is a Docker/Kubernetes training workspace made of **standalone exercises**, not one integrated application.
- Work from the relevant subdirectory (`1-cwiczenie`, `2-cwiczenia`, `3-cwiczenie`, `4-cwiczenie`, `5-cwiczenie`, `6-cwiczenia`, `projekt-compose`) instead of assuming repo-root commands.
- The root `main.py` is a PyCharm sample file and is usually unrelated to the exercises.
- Existing READMEs and learner-facing examples are in **Polish**; keep new docs and visible app text aligned unless asked to switch language.

## Build, test, and lint commands

| Area | Commands |
| --- | --- |
| `1-cwiczenie` | `cd 1-cwiczenie && npm install && npm start`<br>`cd 1-cwiczenie && docker build -t node-basic . && docker run --rm -p 3000:3000 node-basic`<br>Manual check: `curl http://localhost:3000/` |
| `2-cwiczenia` | `cd 2-cwiczenia && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python app.py`<br>`cd 2-cwiczenia && docker build -t flask-students-app . && docker run --rm -p 5000:5000 flask-students-app`<br>Manual checks: `curl http://localhost:5000/` and `curl http://localhost:5000/health` |
| `3-cwiczenie` | `cd 3-cwiczenie && docker build -t fastapi-basic .`<br>`cd 3-cwiczenie && docker build -f Dockerfile_z_multistage -t fastapi-multistage .`<br>`cd 3-cwiczenie && docker run --rm -p 8000:8000 fastapi-basic`<br>`cd 3-cwiczenie && docker run --rm -p 8000:8000 fastapi-multistage`<br>Manual check: `curl http://localhost:8000/` |
| `4-cwiczenie` | `cd 4-cwiczenie && docker compose up --build`<br>`cd 4-cwiczenie && docker compose ps`<br>`cd 4-cwiczenie && docker compose logs web`<br>`cd 4-cwiczenie && docker compose exec redis redis-cli GET visits`<br>`cd 4-cwiczenie && docker compose down` or `docker compose down -v`<br>Manual checks: `curl http://localhost:8080/` and `curl http://localhost:8080/health` |
| `5-cwiczenie` | `cd 5-cwiczenie && docker compose up --build`<br>`cd 5-cwiczenie && docker compose run --rm tests pytest tests/unit -q`<br>`cd 5-cwiczenie && docker compose run --rm tests pytest tests/unit/test_logic.py::test_build_status_payload_returns_ok -q`<br>`cd 5-cwiczenie && docker compose --profile tests up --build --abort-on-container-exit --exit-code-from tests tests`<br>`cd 5-cwiczenie && docker compose up --build -d && docker compose run --rm tests pytest tests/integration/test_endpoints.py::test_health_endpoint_reports_redis_connection -q`<br>`cd 5-cwiczenie && docker compose -f docker-compose.dockerfile-healthcheck.yml up --build -d`<br>Manual checks: `curl http://localhost:8081/health`, `curl http://localhost:8081/diag`, `curl http://localhost:8081/metrics` |
| `6-cwiczenia` | `cd 6-cwiczenia/app && docker build -t lab6-app-image .`<br>`cd 6-cwiczenia/app && docker run --rm lab6-app-image pytest tests/unit -q`<br>`cd 6-cwiczenia/app && docker run --rm lab6-app-image pytest tests/unit/test_logic.py::test_build_status_payload_returns_ok -q`<br>`docker run --rm --network lab6-network -e APP_BASE_URL=http://lab6-app:5000 lab6-app-image pytest tests/integration -q`<br>`docker run --rm --network lab6-network -e APP_BASE_URL=http://lab6-app:5000 lab6-app-image pytest tests/integration/test_endpoints.py::test_health_endpoint_reports_redis_connection -q`<br>Prereq runtime setup: create `lab6-network`, run `lab6-redis`, then run `lab6-app` on `8082:5000` as documented in `6-cwiczenia/README.md`<br>Manual checks: `curl http://localhost:8082/health`, `curl http://localhost:8082/diag`, `curl http://localhost:8082/metrics` |
| `projekt-compose` | `cd projekt-compose && docker compose up --build`<br>`cd projekt-compose && docker compose ps`<br>`cd projekt-compose && docker compose logs web`<br>`cd projekt-compose && docker compose logs db`<br>`cd projekt-compose && docker compose exec db psql -U appuser -d appdb`<br>`cd projekt-compose && docker compose down` or `docker compose down -v`<br>Manual check: `curl http://localhost:8000/` |

There is no repository-wide lint configuration. Do not assume `npm test`, `pytest`, or lint commands exist outside `5-cwiczenie` and `6-cwiczenia`.

## High-level architecture

- The repository is a progression of Docker exercises: `1-cwiczenie` is a single-file Node HTTP server, `2-cwiczenia` is a single-service Flask app, and `3-cwiczenie` keeps the app tiny while comparing a classic Docker build with a multistage build for the same FastAPI package.
- `4-cwiczenie` and `projekt-compose` are the main Compose-based service-discovery examples. `4-cwiczenie` wires Flask to Redis for a visit counter, while `projekt-compose` wires Flask to PostgreSQL and shows named volume persistence plus startup retry behavior when the database is not ready yet.
- `5-cwiczenie` and `6-cwiczenia` are parallel versions of the same observability/testing exercise: Flask app + Redis + `/health` + `/diag` + `/metrics` + helper logic in `logic.py` + unit and integration tests. The difference is orchestration: `5-cwiczenie` uses Compose, health-gated dependencies, and a `tests` profile; `6-cwiczenia` does the same work with raw `docker build`, `docker run`, a manual Docker network, and a `HEALTHCHECK` baked into the image.
- In `5-cwiczenie`, `docker-compose.dockerfile-healthcheck.yml` is intentionally paired with the main Compose file to demonstrate the difference between defining health checks in Compose versus inheriting them from the image.

## Key conventions

- Treat each exercise directory as self-contained: dependencies, Docker context, ports, and commands are local to that folder.
- Preserve the established port mapping conventions: `3000` (`1-cwiczenie`), `5000` (`2-cwiczenia`), `8000` (`3-cwiczenie` and `projekt-compose`), `8080` (`4-cwiczenie`), `8081` (`5-cwiczenie`), and `8082` (`6-cwiczenia`).
- Keep service-to-service connections on Docker service/container names, not `localhost`: `redis` in Compose exercises, `db` in `projekt-compose`, and `lab6-redis` / `lab6-app` in `6-cwiczenia`.
- In `projekt-compose`, keep database settings synchronized between `docker-compose.yml` and `web/app.py` defaults (`DB_HOST=db`, `DB_NAME=appdb`, `DB_USER=appuser`, `DB_PASSWORD=secret`).
- In `projekt-compose` and the Redis-based exercises, retry loops and health-based startup ordering are intentional. Do not simplify them away unless the exercise goal changes.
- In `3-cwiczenie`, update both `Dockerfile` and `Dockerfile_z_multistage` together whenever startup, copied files, or dependency handling changes; they are meant to stay functionally equivalent apart from build strategy.
- `5-cwiczenie` and `6-cwiczenia` intentionally mirror each other. If you change endpoint payloads, helper logic, healthcheck scripts, or test expectations in one, check whether the matching exercise should stay aligned.
- In `5-cwiczenie` and `6-cwiczenia`, the app image also serves as the test runner image because `requirements-dev.txt` is installed alongside runtime dependencies.
- Keep visible UI text and documentation in Polish unless the task explicitly calls for another language.
