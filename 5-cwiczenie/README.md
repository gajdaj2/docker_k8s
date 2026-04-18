# 5-cwiczenie - Testowanie kontenerow, health checks i diagnostyka

To cwiczenie wprowadza podstawy testowania aplikacji uruchamianych w kontenerach oraz pokazuje, jak wdrozyc health checks i podstawowa diagnostyke.

## Cele modulu

Po wykonaniu tego cwiczenia student powinien:

- rozumiec roznice miedzy unit testami i integration testami w kontekscie kontenerow
- umiec uruchomic testy w kontenerze i w srodowisku Docker Compose
- rozumiec zastosowanie health checks typu CMD, HTTP i TCP
- umiec sprawdzac logi i podstawowe metryki aplikacji
- potrafic samodzielnie wdrozyc health checks w prostym projekcie

## Zawartosc modulu

1. Unit testy w Docker
2. Integration testy dla kontenerow
3. Health checks: CMD, HTTP, TCP
4. Monitorowanie logow i metryki
5. LAB: Implementacja health checks

## 1. Struktura projektu

```text
5-cwiczenie/
+-- docker-compose.yml
+-- app/
    +-- Dockerfile
    +-- app.py
    +-- healthcheck_http.py
    +-- healthcheck_tcp.py
    +-- logic.py
    +-- requirements.txt
    +-- requirements-dev.txt
    +-- tests/
        +-- integration/
        |   +-- test_endpoints.py
        +-- unit/
            +-- test_logic.py
```

Najwazniejsze elementy:

- `docker-compose.yml` - uruchamia aplikacje, Redis i opcjonalny serwis testowy
- `docker-compose.dockerfile-healthcheck.yml` - wariant, w ktorym serwis `app` nie ma `healthcheck` w Compose, bo dziedziczy go z `Dockerfile`
- `app/app.py` - aplikacja Flask z endpointami `/`, `/health`, `/diag`, `/metrics`
- `app/logic.py` - logika pomocnicza do unit testow
- `app/healthcheck_http.py` - skrypt sprawdzajacy endpoint HTTP
- `app/healthcheck_tcp.py` - skrypt sprawdzajacy polaczenie TCP
- `app/tests/unit/` - szybkie testy logiki aplikacji
- `app/tests/integration/` - testy sprawdzajace dzialanie uruchomionej uslugi

## 2. Architektura srodowiska

Srodowisko sklada sie z trzech serwisow:

- `app` - aplikacja Flask uruchamiana w kontenerze
- `redis` - zewnetrzny serwis do przechowywania licznika odwiedzin
- `tests` - serwis uruchamiany tylko na profilu `tests`, wykonujacy `pytest`

Przeplyw dzialania:

1. `redis` startuje jako pierwszy i przechodzi health check.
2. `app` startuje po zdrowym Redis i udostepnia HTTP na porcie `8081`.
3. `tests` moze zostac uruchomiony po starcie `app` i `redis`, aby wykonac unit i integration testy.

## 3. Plik `docker-compose.yml`

```yaml
services:
  app:
    build: ./app
    ports:
      - "8081:5000"
    environment:
      REDIS_HOST: redis
      APP_TITLE: Testowanie i health checks
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "healthcheck_http.py"]

  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]

  tests:
    build: ./app
    environment:
      APP_BASE_URL: http://app:5000
    command: ["pytest", "tests/unit", "tests/integration", "-q"]
    depends_on:
      app:
        condition: service_healthy
      redis:
        condition: service_healthy
    profiles: ["tests"]
```

Znaczenie najwazniejszych ustawien:

- `depends_on.condition: service_healthy` - uruchamia zalezne uslugi dopiero po przejsciu health checka
- `healthcheck.test` - okresla komenda sprawdzajaca zdrowie kontenera
- `profiles: ["tests"]` - testy uruchamiaja sie tylko wtedy, gdy jawnie wlaczysz profil `tests`
- `command: ["pytest", ...]` - serwis `tests` nie uruchamia aplikacji, tylko wykonuje testy

### Wariant: brak `healthcheck` w Compose, ale jest w `Dockerfile`

W projekcie znajduje sie tez plik:

```text
docker-compose.dockerfile-healthcheck.yml
```

W tym wariancie serwis `app` nie definiuje `healthcheck` w `docker-compose`, poniewaz obraz ma juz wpis:

```dockerfile
HEALTHCHECK CMD ["python", "healthcheck_http.py"]
```

To oznacza, ze Docker Compose nadal zobaczy status `healthy`, mimo ze sama sekcja `healthcheck:` nie wystepuje przy serwisie `app` w pliku Compose.

Uruchomienie tego wariantu:

```bash
cd 5-cwiczenie
docker compose -f docker-compose.dockerfile-healthcheck.yml up --build -d
docker compose -f docker-compose.dockerfile-healthcheck.yml ps
```

Opis komend:

- `cd 5-cwiczenie` - przechodzi do katalogu projektu
- `docker compose -f docker-compose.dockerfile-healthcheck.yml up --build -d` - uruchamia wariant srodowiska, w ktorym `app` korzysta z health checka odziedziczonego z obrazu
- `docker compose -f docker-compose.dockerfile-healthcheck.yml ps` - pokazuje status kontenerow i pozwala sprawdzic, czy `app` osiagnal status `healthy`

## 4. Uruchomienie aplikacji

W katalogu `5-cwiczenie` wykonaj:

```bash
cd 5-cwiczenie
docker compose up --build
```

Opis komend:

- `cd 5-cwiczenie` - przechodzi do katalogu z plikiem `docker-compose.yml`
- `docker compose up --build` - buduje obraz aplikacji, uruchamia `app` i `redis`, a nastepnie pokazuje logi

Po uruchomieniu aplikacja bedzie dostepna pod adresami:

- http://localhost:8081/
- http://localhost:8081/health
- http://localhost:8081/diag
- http://localhost:8081/metrics

## 5. Unit testy w Docker

Unit testy sprawdzaja male fragmenty logiki bez potrzeby uruchamiania calego systemu.

Pelny zestaw unit testow:

```bash
cd 5-cwiczenie
docker compose run --rm tests pytest tests/unit -q
```

Opis komend:

- `cd 5-cwiczenie` - przechodzi do katalogu projektu
- `docker compose run --rm tests pytest tests/unit -q` - uruchamia tymczasowy kontener `tests` i wykonuje tylko unit testy

Uruchomienie pojedynczego testu:

```bash
docker compose run --rm tests pytest tests/unit/test_logic.py::test_build_status_payload_returns_ok -q
```

Opis komendy:

- `docker compose run --rm tests pytest tests/unit/test_logic.py::test_build_status_payload_returns_ok -q` - wykonuje jeden wskazany test z pliku `test_logic.py`

## 6. Integration testy dla kontenerow

Integration testy sprawdzaja wspolprace dzialajacych uslug.

Pelne uruchomienie wszystkich testow:

```bash
cd 5-cwiczenie
docker compose --profile tests up --build --abort-on-container-exit --exit-code-from tests tests
```

Opis komend:

- `cd 5-cwiczenie` - przechodzi do katalogu projektu
- `docker compose --profile tests up --build --abort-on-container-exit --exit-code-from tests tests` - buduje obrazy, uruchamia `redis`, `app` i `tests`, a po zakonczeniu testow zwraca wynik serwisu testowego i zatrzymuje caly zestaw

Uruchomienie pojedynczego testu integracyjnego:

Najpierw uruchom aplikacje w tle:

```bash
docker compose up --build -d
```

Nastepnie wykonaj jeden test:

```bash
docker compose run --rm tests pytest tests/integration/test_endpoints.py::test_health_endpoint_reports_redis_connection -q
```

Opis komend:

- `docker compose up --build -d` - uruchamia srodowisko w tle
- `docker compose run --rm tests pytest tests/integration/test_endpoints.py::test_health_endpoint_reports_redis_connection -q` - wykonuje jeden integration test przeciwko uruchomionej aplikacji

## 7. Health checks: CMD, HTTP, TCP

### Health check typu CMD

Przyklad:

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
```

Ten health check uruchamia komende wewnatrz kontenera Redis. Jesli `redis-cli ping` zwroci sukces, kontener jest uznany za zdrowy.

### Health check typu HTTP

Przyklad z tego cwiczenia:

```yaml
healthcheck:
  test: ["CMD", "python", "healthcheck_http.py"]
```

Skrypt `healthcheck_http.py` wysyla zapytanie do:

```text
http://127.0.0.1:5000/health
```

Jesli aplikacja odpowie kodem `200`, health check przechodzi poprawnie.

Reczne sprawdzenie:

```bash
docker compose exec app python healthcheck_http.py
curl http://localhost:8081/health
```

Opis komend:

- `docker compose exec app python healthcheck_http.py` - uruchamia skrypt health checka HTTP wewnatrz kontenera aplikacji
- `curl http://localhost:8081/health` - sprawdza endpoint zdrowia z poziomu hosta

### Health check typu TCP

W Compose nie ma osobnego slowa kluczowego `tcp`, ale mozna wykonac test TCP przez komende.

Przyklad reczny:

```bash
docker compose exec app python healthcheck_tcp.py redis 6379
```

Opis komendy:

- `docker compose exec app python healthcheck_tcp.py redis 6379` - sprawdza, czy z kontenera `app` mozna otworzyc polaczenie TCP do serwisu `redis` na porcie `6379`

## 8. Health checks i diagnostyka

Przydatne polecenia:

```bash
docker compose ps
docker compose logs
docker compose logs app
docker compose logs redis
docker inspect --format='{{json .State.Health}}' 5-cwiczenie-app-1
curl http://localhost:8081/diag
curl http://localhost:8081/metrics
```

Opis komend:

- `docker compose ps` - pokazuje stan kontenerow
- `docker compose logs` - wyswietla logi wszystkich uslug
- `docker compose logs app` - wyswietla logi aplikacji
- `docker compose logs redis` - wyswietla logi Redis
- `docker inspect --format='{{json .State.Health}}' 5-cwiczenie-app-1` - pokazuje szczegoly ostatnich prob health checka kontenera aplikacji
- `curl http://localhost:8081/diag` - pobiera podstawowe dane diagnostyczne aplikacji
- `curl http://localhost:8081/metrics` - pobiera metryki w formacie Prometheus

## 9. Monitorowanie logow i metryki

W tym projekcie monitorowanie realizowane jest na dwa sposoby:

- **logi** - przez `docker compose logs`, gdzie widac start aplikacji, bledy i wywolania
- **metryki** - przez endpoint `/metrics`, gdzie publikowany jest licznik `page_visits_total`

Przykladowe sprawdzenie:

```bash
curl http://localhost:8081/
curl http://localhost:8081/
curl http://localhost:8081/metrics
```

Opis komend:

- pierwsze dwa wywolania `curl` zwiekszaja licznik odwiedzin
- `curl http://localhost:8081/metrics` - pokazuje aktualna wartosc metryk aplikacji

## 10. LAB: Implementacja health checks

### Zadanie 1

Uruchom srodowisko i sprawdz, czy `app` oraz `redis` maja status healthy.

**Rozwiazanie:**

```bash
cd 5-cwiczenie
docker compose up --build -d
docker compose ps
```

- `cd 5-cwiczenie` - przechodzi do katalogu projektu
- `docker compose up --build -d` - uruchamia srodowisko w tle
- `docker compose ps` - pokazuje status kontenerow, w tym informacje o health checkach

### Zadanie 2

Uruchom tylko unit testy w kontenerze.

**Rozwiazanie:**

```bash
docker compose run --rm tests pytest tests/unit -q
```

- `docker compose run --rm tests pytest tests/unit -q` - uruchamia kontener testowy i wykonuje tylko unit testy

### Zadanie 3

Uruchom pelne testy integracyjne dla wszystkich kontenerow.

**Rozwiazanie:**

```bash
docker compose --profile tests up --build --abort-on-container-exit --exit-code-from tests tests
```

- `docker compose --profile tests up --build --abort-on-container-exit --exit-code-from tests tests` - buduje srodowisko i wykonuje unit oraz integration testy w serwisie `tests`

### Zadanie 4

Sprawdz health check HTTP oraz recznie odczytaj endpoint zdrowia.

**Rozwiazanie:**

```bash
docker compose exec app python healthcheck_http.py
curl http://localhost:8081/health
```

- `docker compose exec app python healthcheck_http.py` - uruchamia skrypt health checka HTTP wewnatrz kontenera
- `curl http://localhost:8081/health` - pokazuje odpowiedz endpointu `/health`

### Zadanie 5

Uruchom wariant, w ktorym `app` nie ma sekcji `healthcheck` w `docker-compose`, ale health check jest zdefiniowany w `Dockerfile`.

**Rozwiazanie:**

```bash
docker compose down -v
docker compose -f docker-compose.dockerfile-healthcheck.yml up --build -d
docker compose -f docker-compose.dockerfile-healthcheck.yml ps
```

- `docker compose down -v` - sprzata poprzednio uruchomione srodowisko
- `docker compose -f docker-compose.dockerfile-healthcheck.yml up --build -d` - uruchamia wariant oparty na health checku z `Dockerfile`
- `docker compose -f docker-compose.dockerfile-healthcheck.yml ps` - pokazuje, ze `app` nadal moze osiagnac status `healthy`

### Zadanie 6

Wykonaj reczny test TCP do serwisu Redis.

**Rozwiazanie:**

```bash
docker compose exec app python healthcheck_tcp.py redis 6379
```

- `docker compose exec app python healthcheck_tcp.py redis 6379` - sprawdza polaczenie TCP z Redis

### Zadanie 7

Sprawdz logi aplikacji i metryki po kilku wywolaniach strony glownej.

**Rozwiazanie:**

```bash
curl http://localhost:8081/
curl http://localhost:8081/
docker compose logs app
curl http://localhost:8081/metrics
```

- kolejne wywolania `curl http://localhost:8081/` zwiekszaja licznik odwiedzin
- `docker compose logs app` - pokazuje logi aplikacji
- `curl http://localhost:8081/metrics` - pokazuje aktualne metryki aplikacji

### Zadanie 8

Zatrzymaj srodowisko i usun dane Redis.

**Rozwiazanie:**

```bash
docker compose down -v
```

- `docker compose down -v` - zatrzymuje kontenery i usuwa takze wolumen z danymi

## 11. Pytania kontrolne

1. Czym roznia sie unit testy od integration testow?
2. Dlaczego serwis `tests` uruchamiany jest przez profil `tests`?
3. Po co w Compose uzywamy `depends_on.condition: service_healthy`?
4. Czym rozni sie sprawdzenie CMD od HTTP?
5. W jaki sposob wykonac test TCP, jesli aplikacja nie ma endpointu HTTP?
6. Do czego sluzy endpoint `/metrics`?

## 12. Zatrzymanie srodowiska

Jesli srodowisko dziala w aktualnym terminalu, zatrzymasz je skrotem:

```text
Ctrl + C
```

Jesli srodowisko dziala w tle:

```bash
docker compose down
```

- `docker compose down` - zatrzymuje i usuwa kontenery oraz siec projektu
