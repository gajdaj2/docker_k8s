# 4-cwiczenie - Docker Compose od podstaw

To cwiczenie pokazuje, jak uruchomic proste srodowisko zlozone z dwoch uslug za pomoca `docker compose`.

## 1. Cel cwiczenia

W tym zadaniu uruchomisz srodowisko skladajace sie z:

- `web` - aplikacji Flask uruchamianej w kontenerze
- `redis` - gotowego serwisu Redis

Aplikacja `web` laczy sie z usluga `redis` i zapisuje liczbe odwiedzin strony. Dzięki temu zobaczysz, jak dwa kontenery wspolpracuja w jednym srodowisku Compose.

## 2. Struktura katalogu

```text
4-cwiczenie/
├── docker-compose.yml
└── web/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

- `docker-compose.yml` - opisuje cale srodowisko
- `web/Dockerfile` - buduje obraz dla aplikacji web
- `web/app.py` - prosta aplikacja Flask
- `web/requirements.txt` - zaleznosci Pythona

## 3. Jak dziala to srodowisko

Po uruchomieniu `docker compose`:

1. budowany jest obraz dla serwisu `web`
2. pobierany jest gotowy obraz `redis:7-alpine`
3. oba kontenery trafiaja do jednej domyslnej sieci
4. aplikacja `web` laczy sie z Redis po nazwie uslugi `redis`
5. dane Redis sa zapisywane w wolumenie `redis_data`

## 4. Plik `docker-compose.yml`

```yaml
services:
  web:
    build: ./web
    ports:
      - "8080:5000"
    environment:
      REDIS_HOST: redis
      APP_TITLE: Docker Compose od podstaw
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

Znaczenie najwazniejszych elementow:

- `services` - lista uslug, ktore maja zostac uruchomione
- `web` - serwis budowany z lokalnego katalogu `./web`
- `build: ./web` - nakazuje zbudowac obraz na podstawie `web/Dockerfile`
- `ports: "8080:5000"` - udostepnia port 5000 z kontenera na porcie 8080 hosta
- `environment` - przekazuje zmienne srodowiskowe do kontenera
- `REDIS_HOST: redis` - aplikacja laczy sie z Redis po nazwie uslugi Compose
- `depends_on` - uruchamia serwis `web` po uruchomieniu serwisu `redis`
- `image: redis:7-alpine` - uzywa gotowego obrazu Redis
- `volumes` - tworzy trwaly wolumen na dane uslugi Redis

## 5. Plik `web/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

Znaczenie polecen:

- `FROM python:3.11-slim` - wybiera lekki obraz z Pythonem 3.11
- `WORKDIR /app` - ustawia katalog roboczy wewnatrz kontenera
- `COPY requirements.txt .` - kopiuje plik z zaleznosciami
- `RUN pip install --no-cache-dir -r requirements.txt` - instaluje Flask i Redis client
- `COPY app.py .` - kopiuje plik aplikacji do kontenera
- `EXPOSE 5000` - informuje, ze aplikacja nasluchuje na porcie 5000
- `CMD ["python", "app.py"]` - uruchamia aplikacje po starcie kontenera

## 6. Uruchomienie srodowiska

W katalogu `4-cwiczenie` wykonaj:

```bash
cd 4-cwiczenie
docker compose up --build
```

Opis komend:

- `cd 4-cwiczenie` - przechodzi do katalogu z plikiem `docker-compose.yml`
- `docker compose up --build` - buduje obraz serwisu `web`, uruchamia wszystkie uslugi i pokazuje logi w terminalu

Po uruchomieniu aplikacja bedzie dostepna pod adresem:

- http://localhost:8080/
- http://localhost:8080/health

## 7. Sprawdzenie dzialania

W nowym terminalu uruchom:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
```

Opis komend:

- `curl http://localhost:8080/` - wysyla zapytanie do aplikacji web i pokazuje strone w terminalu
- `curl http://localhost:8080/health` - sprawdza, czy aplikacja i polaczenie z Redis dzialaja poprawnie

Po odswiezeniu strony kilka razy liczba odwiedzin powinna rosnac.

## 8. Przydatne polecenia Docker Compose

```bash
docker compose ps
docker compose logs
docker compose logs web
docker compose logs redis
docker compose exec redis redis-cli GET visits
docker compose down
docker compose down -v
```

Opis komend:

- `docker compose ps` - pokazuje uruchomione kontenery w tym srodowisku
- `docker compose logs` - wyswietla logi wszystkich uslug
- `docker compose logs web` - wyswietla logi tylko aplikacji web
- `docker compose logs redis` - wyswietla logi tylko serwisu Redis
- `docker compose exec redis redis-cli GET visits` - uruchamia `redis-cli` w kontenerze Redis i odczytuje zapisany licznik odwiedzin
- `docker compose down` - zatrzymuje i usuwa kontenery oraz siec
- `docker compose down -v` - dodatkowo usuwa wolumen z danymi Redis

## 9. Zadania do wykonania

### Zadanie 1

Uruchom cale srodowisko za pomoca Docker Compose.

**Rozwiazanie:**

```bash
cd 4-cwiczenie
docker compose up --build
```

- `cd 4-cwiczenie` - przechodzi do katalogu z konfiguracja Compose
- `docker compose up --build` - buduje i uruchamia uslugi `web` oraz `redis`

### Zadanie 2

Sprawdz, czy aplikacja dziala w przegladarce i przez `curl`.

**Rozwiazanie:**

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
```

- `curl http://localhost:8080/` - pobiera glowna strone aplikacji
- `curl http://localhost:8080/health` - sprawdza stan aplikacji i polaczenia z Redis

### Zadanie 3

Sprawdz, jakie kontenery uruchomilo Compose i podejrzyj ich logi.

**Rozwiazanie:**

```bash
docker compose ps
docker compose logs
```

- `docker compose ps` - pokazuje aktywne kontenery dla tego projektu
- `docker compose logs` - wyswietla logi wszystkich uslug w jednym miejscu

### Zadanie 4

Sprawdz, czy licznik odwiedzin jest zapisywany w Redis.

**Rozwiazanie:**

Najpierw wejdz kilka razy na strone:

```bash
curl http://localhost:8080/
curl http://localhost:8080/
curl http://localhost:8080/
```

Nastepnie sprawdz wartosc w Redis:

```bash
docker compose exec redis redis-cli GET visits
```

- kolejne polecenia `curl` zwiekszaja licznik odwiedzin
- `docker compose exec redis redis-cli GET visits` - odczytuje aktualna wartosc klucza `visits` z serwisu Redis

### Zadanie 5

Zmien mapowanie portow tak, aby aplikacja byla dostepna pod adresem `http://localhost:8090`.

**Rozwiazanie:**

W pliku `docker-compose.yml` zmien:

```yaml
ports:
  - "8080:5000"
```

na:

```yaml
ports:
  - "8090:5000"
```

Nastepnie uruchom ponownie srodowisko:

```bash
docker compose down
docker compose up --build
```

- edycja `ports` zmienia port hosta z 8080 na 8090
- `docker compose down` - zatrzymuje poprzednia wersje srodowiska
- `docker compose up --build` - uruchamia srodowisko z nowa konfiguracja

### Zadanie 6

Sprawdz, czy dane w Redis sa trwale, dopoki nie usuniesz wolumenu.

**Rozwiazanie:**

1. Odwiedz kilka razy strone `http://localhost:8080/` lub `http://localhost:8090/`.
2. Sprawdz licznik:

```bash
docker compose exec redis redis-cli GET visits
```

3. Zatrzymaj srodowisko bez usuwania wolumenu:

```bash
docker compose down
```

4. Uruchom je ponownie:

```bash
docker compose up --build
```

5. Jeszcze raz sprawdz licznik:

```bash
docker compose exec redis redis-cli GET visits
```

6. Usun dane razem z wolumenem:

```bash
docker compose down -v
```

Znaczenie komend:

- `docker compose exec redis redis-cli GET visits` - pokazuje aktualny licznik zapisany w Redis
- `docker compose down` - zatrzymuje srodowisko, ale zostawia wolumen z danymi
- `docker compose up --build` - uruchamia uslugi ponownie
- `docker compose down -v` - usuwa kontenery, siec i wolumen, czyli takze zapisane dane

## 10. Pytania kontrolne

1. Do czego sluzy plik `docker-compose.yml`?
2. Czym rozni sie `build` od `image`?
3. Dlaczego aplikacja laczy sie z Redis po nazwie `redis`, a nie `localhost`?
4. Co robi `depends_on`?
5. Po co uzywamy wolumenu `redis_data`?
6. Czym rozni sie `docker compose down` od `docker compose down -v`?

## 11. Zatrzymanie srodowiska

Jesli srodowisko dziala w aktualnym terminalu, zatrzymasz je skrotem:

```text
Ctrl + C
```

Jesli chcesz zatrzymac je z innego terminala, uzyj:

```bash
docker compose down
```

- `docker compose down` - zatrzymuje i usuwa kontenery utworzone przez Compose
