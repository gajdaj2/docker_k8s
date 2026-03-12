 Ćwiczenie z Docker Compose

To ćwiczenie pokazuje, jak uruchomić prostą aplikację webową oraz bazę danych PostgreSQL za pomocą `docker compose`.

## Cel ćwiczenia

Uruchom środowisko złożone z dwóch serwisów:

- `web` — prosta aplikacja Python/Flask
- `db` — PostgreSQL 16

Aplikacja `web` ma połączyć się z bazą `db` i po wejściu na stronę wyświetlić informację, że połączenie działa.

---

## Struktura projektu

Struktura katalogów i plików projektu:

```text
projekt-compose/
├── docker-compose.yml
└── web/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

---

## Plik `docker-compose.yml`

Głównym plik `docker-compose.yml`:

```yaml
services:
  web:
    build: ./web
    ports:
      - "8000:8000"
    environment:
      DB_HOST: db
      DB_NAME: appdb
      DB_USER: appuser
      DB_PASSWORD: secret
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:

networks:
  default:
    name: szkolenie-compose-net
```

---

## Plik `web/Dockerfile`

Plik `web/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
```

---

## Plik `web/requirements.txt`

Plik `web/requirements.txt`:

```txt
flask==3.0.3
psycopg2-binary==2.9.9
```

---

## Plik `web/app.py`

Plik `web/app.py`:

```python
import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def home():
    retries = 5
    last_error = ""

    while retries > 0:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT version();")
            db_version = cur.fetchone()[0]
            cur.close()
            conn.close()

            return f\"\"\"
            <h1>Aplikacja działa</h1>
            <p>Połączenie z bazą PostgreSQL zostało nawiązane.</p>
            <p><b>Wersja bazy:</b> {db_version}</p>
            \"\"\"
        except Exception as e:
            last_error = str(e)
            retries -= 1
            time.sleep(2)

    return f"<h1>Błąd połączenia z bazą</h1><p>{last_error}</p>", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

## Instrukcja wykonania ćwiczenia

### Krok 1. Praca z projektem


```bash
cd projekt-compose
```
---

### Krok 2. Uruchom środowisko

W katalogu głównym projektu wykonaj:

```bash
docker compose up --build
```

To polecenie:

- zbuduje obraz dla serwisu `web`
- pobierze obraz `postgres:16` dla serwisu `db`
- utworzy sieć `szkolenie-compose-net`
- utworzy wolumen `pgdata`
- uruchomi oba kontenery

---

### Krok 3. Sprawdź działanie aplikacji

Otwórz przeglądarkę i przejdź pod adres:

```text
http://localhost:8000
```

Powinien pojawić się komunikat:

- `Aplikacja działa`
- informacja o połączeniu z bazą PostgreSQL
- wersja bazy danych

---

### Krok 4. Sprawdź stan kontenerów

Wyświetl uruchomione kontenery:

```bash
docker compose ps
```

Sprawdź logi wszystkich usług:

```bash
docker compose logs
```

Sprawdź logi tylko aplikacji web:

```bash
docker compose logs web
```

Sprawdź logi tylko bazy danych:

```bash
docker compose logs db
```

---

### Krok 5. Wejdź do kontenera bazy danych

Uruchom klienta `psql` w kontenerze `db`:

```bash
docker compose exec db psql -U appuser -d appdb
```

Przykładowe polecenia SQL:

```sql
CREATE TABLE test (
  id SERIAL PRIMARY KEY,
  name TEXT
);

INSERT INTO test (name) VALUES ('Ala');
SELECT * FROM test;
```

Wyjście z `psql`:

```sql
\q
```

---

### Krok 6. Zatrzymaj środowisko

Zatrzymanie i usunięcie kontenerów oraz sieci:

```bash
docker compose down
```

Zatrzymanie i usunięcie kontenerów, sieci oraz wolumenu z danymi:

```bash
docker compose down -v
```

---

## Omówienie konfiguracji

### Serwis `web`

```yaml
web:
  build: ./web
```

Serwis `web` budowany jest z lokalnego katalogu `./web`, w którym znajduje się `Dockerfile`.

```yaml
ports:
  - "8000:8000"
```

Port `8000` na komputerze hosta jest mapowany na port `8000` w kontenerze.

```yaml
environment:
  DB_HOST: db
```

Aplikacja korzysta ze zmiennych środowiskowych do połączenia z bazą danych.  
Wartość `db` oznacza nazwę serwisu w sieci Dockera, a nie `localhost`.

```yaml
depends_on:
  - db
```

Serwis `web` startuje po serwisie `db`, ale warto pamiętać, że `depends_on` nie gwarantuje pełnej gotowości bazy do przyjmowania połączeń.  
Dlatego w aplikacji zastosowano kilka prób połączenia.

---

### Serwis `db`

```yaml
db:
  image: postgres:16
```

Serwis `db` korzysta z gotowego obrazu PostgreSQL 16 z Docker Hub.

```yaml
environment:
  POSTGRES_DB: appdb
  POSTGRES_USER: appuser
  POSTGRES_PASSWORD: secret
```

Zmienne środowiskowe inicjalizują bazę danych oraz konto użytkownika.

```yaml
volumes:
  - pgdata:/var/lib/postgresql/data
```

Dane PostgreSQL są zapisywane w wolumenie `pgdata`, dzięki czemu nie znikają po restarcie kontenera.

---

### Wolumeny

```yaml
volumes:
  pgdata:
```

Definicja wolumenu Dockera do trwałego przechowywania danych bazy.

---

### Sieć

```yaml
networks:
  default:
    name: szkolenie-compose-net
```

Tworzona jest domyślna sieć o nazwie `szkolenie-compose-net`, dzięki której kontenery mogą komunikować się po nazwach usług, np. `web` może łączyć się z `db`.

---

## Czy potrzebny jest Dockerfile dla bazy?

Nie.  
Dla serwisu `db` używany jest gotowy obraz:

```yaml
image: postgres:16
```

To oznacza, że osobny `Dockerfile` nie jest potrzebny.

Dockerfile przygotowujemy zwykle wtedy, gdy:

- budujemy własną aplikację
- chcemy rozszerzyć gotowy obraz
- potrzebujemy własnej konfiguracji podczas budowania

---

## Zadania dla uczestnika

### Zadanie 1

Uruchom środowisko i sprawdź, czy aplikacja działa pod adresem `http://localhost:8000`.

### Zadanie 2

Sprawdź, jakie kontenery, sieci i wolumeny zostały utworzone przez `docker compose`.

Pomocnicze polecenia:

```bash
docker ps
docker network ls
docker volume ls
```

### Zadanie 3

Zmień mapowanie portów w serwisie `web` z:

```yaml
ports:
  - "8000:8000"
```

na:

```yaml
ports:
  - "8080:8000"
```

Uruchom środowisko ponownie i sprawdź aplikację pod adresem:

```text
http://localhost:8080
```

### Zadanie 4

Zmień nazwę bazy danych z `appdb` na `szkolenie_db` zarówno w serwisie `web`, jak i `db`.

Uruchom środowisko i sprawdź, czy aplikacja nadal działa.

### Zadanie 5

Sprawdź trwałość danych:

1. uruchom środowisko
2. wejdź do `psql`
3. utwórz tabelę `test`
4. wykonaj `docker compose down`
5. uruchom środowisko ponownie
6. sprawdź, czy tabela nadal istnieje
7. wykonaj `docker compose down -v`
8. uruchom środowisko jeszcze raz i sprawdź, czy tabela zniknęła

---

## Pytania kontrolne

1. Dlaczego w `DB_HOST` wpisujemy `db`, a nie `localhost`?
2. Jaka jest różnica między `build` i `image`?
3. Do czego służy wolumen `pgdata`?
4. Co usuwa polecenie `docker compose down -v`?
5. Czy `depends_on` oznacza, że baza jest od razu gotowa na połączenia?

---

## Szybkie podsumowanie

W tym ćwiczeniu uczysz się:

- definiować wiele usług w `docker compose`
- budować obraz aplikacji z `Dockerfile`
- używać gotowego obrazu PostgreSQL
- mapować porty
- przekazywać zmienne środowiskowe
- korzystać z wolumenów
- uruchamiać i zatrzymywać środowisko wieloserwisowe
- rozumieć komunikację między kontenerami w sieci Dockera
