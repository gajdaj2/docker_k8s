# 6-cwiczenia - Docker bez Compose: testy, health checks i diagnostyka

To cwiczenie pokazuje, jak realizowac testowanie kontenerow, health checks i diagnostyke tylko przy uzyciu polecen Dockera, bez `docker compose`.

## Cele modulu

Po wykonaniu tego cwiczenia student powinien:

- rozumiec roznice miedzy unit testami i integration testami dla kontenerow
- umiec uruchamiac testy przy uzyciu `docker run`
- rozumiec zastosowanie health checks typu CMD, HTTP i TCP
- umiec monitorowac logi oraz metryki kontenera
- potrafic samodzielnie wdrozyc health checks w projekcie bez Docker Compose

## Zawartosc modulu

1. Unit testy w Docker
2. Integration testy dla kontenerow
3. Health checks: CMD, HTTP, TCP
4. Monitorowanie logow i metryki
5. LAB: Implementacja health checks

## 1. Struktura projektu

```text
6-cwiczenia/
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

- `app/Dockerfile` - buduje obraz aplikacji i definiuje `HEALTHCHECK`
- `app/app.py` - aplikacja Flask z endpointami `/`, `/health`, `/diag`, `/metrics`
- `app/logic.py` - wydzielona logika do unit testow
- `app/healthcheck_http.py` - skrypt health checka HTTP
- `app/healthcheck_tcp.py` - skrypt testu TCP
- `app/tests/unit/` - unit testy logiki
- `app/tests/integration/` - integration testy uruchomionej aplikacji

## 2. Architektura srodowiska

W tym cwiczeniu nie ma pliku Compose. Srodowisko skladamy recznie z polecen Dockera:

1. budujemy obraz aplikacji
2. tworzymy siec Docker
3. uruchamiamy kontener Redis
4. uruchamiamy kontener aplikacji
5. uruchamiamy testy w oddzielnych kontenerach

Uzywane elementy:

- `lab6-network` - recznie utworzona siec Docker
- `lab6-redis` - kontener Redis
- `lab6-app` - kontener aplikacji Flask
- obraz `lab6-app-image` - wspolny obraz do uruchamiania aplikacji i testow

## 3. Budowanie obrazu

W katalogu `6-cwiczenia/app` wykonaj:

```bash
cd 6-cwiczenia/app
docker build -t lab6-app-image .
```

Opis komend:

- `cd 6-cwiczenia/app` - przechodzi do katalogu z `Dockerfile`
- `docker build -t lab6-app-image .` - buduje obraz aplikacji i nadaje mu nazwe `lab6-app-image`

## 4. Uruchomienie srodowiska bez Compose

Najpierw utworz siec:

```bash
docker network create lab6-network
```

Opis komendy:

- `docker network create lab6-network` - tworzy wspolna siec, aby kontenery mogly komunikowac sie po nazwach

Uruchom Redis:

```bash
docker run -d --name lab6-redis --network lab6-network --health-cmd "redis-cli ping" --health-interval 10s --health-timeout 3s --health-retries 5 redis:7-alpine redis-server --appendonly yes
```

Opis komendy:

- `docker run -d` - uruchamia kontener w tle
- `--name lab6-redis` - nadaje kontenerowi nazwe `lab6-redis`
- `--network lab6-network` - podlacza kontener do wspolnej sieci
- `--health-cmd "redis-cli ping"` - definiuje health check CMD dla Redis
- `--health-interval 10s` - ustawia odstep miedzy probeami health checka
- `--health-timeout 3s` - ustawia maksymalny czas jednej proby
- `--health-retries 5` - okresla liczbe nieudanych prob przed statusem `unhealthy`
- `redis:7-alpine` - wybiera obraz Redis
- `redis-server --appendonly yes` - uruchamia Redis z zapisem danych

Uruchom aplikacje:

```bash
docker run -d --name lab6-app --network lab6-network -p 8082:5000 -e REDIS_HOST=lab6-redis -e APP_TITLE="Docker bez Compose - testy i health checks" lab6-app-image
```

Opis komendy:

- `docker run -d` - uruchamia aplikacje w tle
- `--name lab6-app` - nadaje kontenerowi nazwe `lab6-app`
- `--network lab6-network` - podlacza kontener do tej samej sieci co Redis
- `-p 8082:5000` - mapuje port 5000 z kontenera na port 8082 hosta
- `-e REDIS_HOST=lab6-redis` - przekazuje nazwe hosta Redis do aplikacji
- `-e APP_TITLE=...` - ustawia tytul wyswietlany na stronie
- `lab6-app-image` - wskazuje obraz, z ktorego startuje kontener

Po uruchomieniu aplikacja bedzie dostepna pod adresami:

- http://localhost:8082/
- http://localhost:8082/health
- http://localhost:8082/diag
- http://localhost:8082/metrics

## 5. Unit testy w Docker

Unit testy uruchamiane sa jako jednorazowy kontener z obrazu aplikacji.

Pelny zestaw unit testow:

```bash
docker run --rm lab6-app-image pytest tests/unit -q
```

Opis komendy:

- `docker run --rm lab6-app-image pytest tests/unit -q` - uruchamia tymczasowy kontener z obrazu aplikacji, wykonuje unit testy i usuwa kontener po zakonczeniu

Pojedynczy test:

```bash
docker run --rm lab6-app-image pytest tests/unit/test_logic.py::test_build_status_payload_returns_ok -q
```

Opis komendy:

- `docker run --rm lab6-app-image pytest tests/unit/test_logic.py::test_build_status_payload_returns_ok -q` - wykonuje tylko jeden wskazany unit test

## 6. Integration testy dla kontenerow

Integration testy sprawdzaja wspolprace uruchomionej aplikacji i Redis w jednej sieci Docker.

Przed uruchomieniem testow integracyjnych warto upewnic sie, ze kontener aplikacji osiagnal status `healthy`.

Sprawdzenie statusu:

```bash
docker inspect --format='{{.State.Health.Status}}' lab6-app
```

Opis komendy:

- `docker inspect --format='{{.State.Health.Status}}' lab6-app` - pokazuje biezacy status health checka kontenera aplikacji

Pelny zestaw integration testow:

```bash
docker inspect --format='{{.State.Health.Status}}' lab6-app
docker run --rm --network lab6-network -e APP_BASE_URL=http://lab6-app:5000 lab6-app-image pytest tests/integration -q
```

Opis komendy:

- `docker inspect --format='{{.State.Health.Status}}' lab6-app` - pozwala sprawdzic, czy aplikacja jest gotowa na testy
- `docker run --rm` - uruchamia tymczasowy kontener testowy
- `--network lab6-network` - podlacza go do sieci, w ktorej dziala aplikacja
- `-e APP_BASE_URL=http://lab6-app:5000` - wskazuje adres aplikacji dostepny z poziomu kontenera testowego
- `lab6-app-image pytest tests/integration -q` - uruchamia integration testy

Pojedynczy test integracyjny:

```bash
docker inspect --format='{{.State.Health.Status}}' lab6-app
docker run --rm --network lab6-network -e APP_BASE_URL=http://lab6-app:5000 lab6-app-image pytest tests/integration/test_endpoints.py::test_health_endpoint_reports_redis_connection -q
```

Opis komendy:

- `docker inspect --format='{{.State.Health.Status}}' lab6-app` - sprawdza, czy kontener aplikacji jest gotowy
- `docker run --rm --network lab6-network -e APP_BASE_URL=http://lab6-app:5000 lab6-app-image pytest tests/integration/test_endpoints.py::test_health_endpoint_reports_redis_connection -q` - wykonuje pojedynczy integration test

## 7. Health checks: CMD, HTTP, TCP

### Health check typu CMD

Przyklad dla Redis:

```bash
docker run -d --name lab6-redis --network lab6-network --health-cmd "redis-cli ping" --health-interval 10s --health-timeout 3s --health-retries 5 redis:7-alpine redis-server --appendonly yes
```

To jest health check CMD, bo Docker uruchamia polecenie `redis-cli ping` wewnatrz kontenera.

### Health check typu HTTP

W `Dockerfile` aplikacji znajduje sie:

```dockerfile
HEALTHCHECK --interval=10s --timeout=3s --retries=5 --start-period=5s CMD ["python", "healthcheck_http.py"]
```

Skrypt `healthcheck_http.py` sprawdza:

```text
http://127.0.0.1:5000/health
```

Reczne sprawdzenie:

```bash
docker exec lab6-app python healthcheck_http.py
curl http://localhost:8082/health
```

Opis komend:

- `docker exec lab6-app python healthcheck_http.py` - uruchamia skrypt health checka HTTP wewnatrz kontenera aplikacji
- `curl http://localhost:8082/health` - pobiera odpowiedz endpointu zdrowia z hosta

### Health check typu TCP

Przyklad reczny:

```bash
docker exec lab6-app python healthcheck_tcp.py lab6-redis 6379
```

Opis komendy:

- `docker exec lab6-app python healthcheck_tcp.py lab6-redis 6379` - sprawdza, czy z kontenera aplikacji mozna otworzyc polaczenie TCP do Redis

## 8. Monitorowanie logow i metryki

Przydatne polecenia:

```bash
docker logs lab6-app
docker logs lab6-redis
docker ps
docker inspect --format='{{json .State.Health}}' lab6-app
curl http://localhost:8082/diag
curl http://localhost:8082/metrics
```

Opis komend:

- `docker logs lab6-app` - wyswietla logi aplikacji
- `docker logs lab6-redis` - wyswietla logi Redis
- `docker ps` - pokazuje dzialajace kontenery i ich porty
- `docker inspect --format='{{json .State.Health}}' lab6-app` - pokazuje szczegoly health checka aplikacji
- `curl http://localhost:8082/diag` - pobiera dane diagnostyczne aplikacji
- `curl http://localhost:8082/metrics` - pobiera metryki w formacie Prometheus

Przykladowe sprawdzenie metryk:

```bash
curl http://localhost:8082/
curl http://localhost:8082/
curl http://localhost:8082/metrics
```

Opis komend:

- dwa pierwsze wywolania `curl` zwiekszaja licznik odwiedzin
- `curl http://localhost:8082/metrics` - pokazuje aktualna wartosc licznika `page_visits_total`

## 9. LAB: Implementacja health checks

### Zadanie 1

Zbuduj obraz aplikacji.

**Rozwiazanie:**

```bash
cd 6-cwiczenia/app
docker build -t lab6-app-image .
```

- `cd 6-cwiczenia/app` - przechodzi do katalogu z Dockerfile
- `docker build -t lab6-app-image .` - buduje obraz aplikacji

### Zadanie 2

Utworz siec Docker i uruchom kontener Redis z health checkiem CMD.

**Rozwiazanie:**

```bash
docker network create lab6-network
docker run -d --name lab6-redis --network lab6-network --health-cmd "redis-cli ping" --health-interval 10s --health-timeout 3s --health-retries 5 redis:7-alpine redis-server --appendonly yes
```

- `docker network create lab6-network` - tworzy siec dla kontenerow
- `docker run ... redis:7-alpine ...` - uruchamia Redis z health checkiem CMD

### Zadanie 3

Uruchom aplikacje Flask i sprawdz, czy odpowiada na porcie `8082`.

**Rozwiazanie:**

```bash
docker run -d --name lab6-app --network lab6-network -p 8082:5000 -e REDIS_HOST=lab6-redis -e APP_TITLE="Docker bez Compose - testy i health checks" lab6-app-image
curl http://localhost:8082/health
```

- `docker run -d --name lab6-app ...` - uruchamia kontener aplikacji w sieci z Redis
- `curl http://localhost:8082/health` - sprawdza, czy aplikacja i Redis dzialaja poprawnie

### Zadanie 4

Uruchom tylko unit testy w osobnym kontenerze.

**Rozwiazanie:**

```bash
docker run --rm lab6-app-image pytest tests/unit -q
```

- `docker run --rm lab6-app-image pytest tests/unit -q` - uruchamia tylko unit testy i usuwa kontener po zakonczeniu

### Zadanie 5

Uruchom integration testy dla dzialajacej aplikacji i Redis.

**Rozwiazanie:**

```bash
docker inspect --format='{{.State.Health.Status}}' lab6-app
docker run --rm --network lab6-network -e APP_BASE_URL=http://lab6-app:5000 lab6-app-image pytest tests/integration -q
```

- `docker inspect --format='{{.State.Health.Status}}' lab6-app` - sprawdza, czy aplikacja uzyskala status `healthy`
- `docker run --rm --network lab6-network -e APP_BASE_URL=http://lab6-app:5000 lab6-app-image pytest tests/integration -q` - wykonuje integration testy przeciwko uruchomionej aplikacji

### Zadanie 6

Sprawdz health check HTTP i wykonaj reczny test TCP.

**Rozwiazanie:**

```bash
docker exec lab6-app python healthcheck_http.py
docker exec lab6-app python healthcheck_tcp.py lab6-redis 6379
```

- `docker exec lab6-app python healthcheck_http.py` - uruchamia sprawdzenie HTTP wewnatrz kontenera
- `docker exec lab6-app python healthcheck_tcp.py lab6-redis 6379` - uruchamia test TCP do Redis

### Zadanie 7

Sprawdz logi i metryki aplikacji po kilku wywolaniach strony glownej.

**Rozwiazanie:**

```bash
curl http://localhost:8082/
curl http://localhost:8082/
docker logs lab6-app
curl http://localhost:8082/metrics
```

- dwa pierwsze wywolania `curl` zwiekszaja licznik odwiedzin
- `docker logs lab6-app` - pokazuje logi aplikacji
- `curl http://localhost:8082/metrics` - pokazuje aktualne metryki

### Zadanie 8

Posprzataj srodowisko po cwiczeniu.

**Rozwiazanie:**

```bash
docker rm -f lab6-app
docker rm -f lab6-redis
docker network rm lab6-network
```

- `docker rm -f lab6-app` - zatrzymuje i usuwa kontener aplikacji
- `docker rm -f lab6-redis` - zatrzymuje i usuwa kontener Redis
- `docker network rm lab6-network` - usuwa recznie utworzona siec

## 10. Pytania kontrolne

1. Czym rozni sie unit test od integration testu?
2. Dlaczego do integration testow potrzebna jest wspolna siec Docker?
3. Czym rozni sie `HEALTHCHECK` w `Dockerfile` od `--health-cmd` w `docker run`?
4. Jak sprawdzic szczegoly health checka kontenera?
5. Po co wystawiac endpoint `/metrics`?

## 11. Zatrzymanie i sprzatanie

Jesli chcesz zatrzymac i usunac srodowisko:

```bash
docker rm -f lab6-app
docker rm -f lab6-redis
docker network rm lab6-network
```

Opis komend:

- `docker rm -f lab6-app` - wymusza zatrzymanie i usuniecie kontenera aplikacji
- `docker rm -f lab6-redis` - wymusza zatrzymanie i usuniecie kontenera Redis
- `docker network rm lab6-network` - usuwa siec Docker utworzona na czas cwiczenia
