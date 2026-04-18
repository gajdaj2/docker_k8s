# Ćwiczenie: multistage build w Docker dla prostej aplikacji FastAPI

## Struktura projektu

Projekt ma następującą strukturę:

```text
3-cwiczenie/
├── app/
│   ├── __init__.py
│   └── main.py
├── Dockerfile
├── Dockerfile_z_multistage
└── requirements.txt
```

## Cel ćwiczenia

Celem ćwiczenia jest:

* uruchomienie prostej aplikacji FastAPI w kontenerze,
* zbudowanie obrazu z klasycznego `Dockerfile`,
* zbudowanie obrazu z pliku `Dockerfile_z_multistage`,
* porównanie obu podejść.

---

## 1. Kod aplikacji

### Plik `app/main.py`

W pliku umieść prostą aplikację:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/health")
def health():
    return {"status": "ok"}
```

### Plik `requirements.txt`

```txt
fastapi
uvicorn
```

---

## 2. Wersja podstawowa — `Dockerfile`

Ten plik służy do zbudowania obrazu w najprostszy sposób.

Przykładowa zawartość:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 3. Wersja multistage — `Dockerfile_z_multistage`

Ten plik pokazuje budowanie obrazu etapami.

Przykładowa zawartość:

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 4. Budowanie obrazu z pliku `Dockerfile`

Przejdź do katalogu projektu:

```bash
cd 3-cwiczenie
```

Zbuduj obraz:

```bash
docker build -t fastapi-basic .
```

Uruchom kontener:

```bash
docker run -p 8000:8000 fastapi-basic
```

Sprawdź w przeglądarce:

```text
http://localhost:8000
```

oraz:

```text
http://localhost:8000/health
```

---

## 5. Budowanie obrazu z pliku `Dockerfile_z_multistage`

Ponieważ plik nie nazywa się `Dockerfile`, trzeba użyć opcji `-f`.

Zbuduj obraz:

```bash
docker build -f Dockerfile_z_multistage -t fastapi-multistage .
```

Uruchom kontener:

```bash
docker run -p 8000:8000 fastapi-multistage
```

Sprawdź działanie aplikacji:

```text
http://localhost:8000
```

oraz:

```text
http://localhost:8000/health
```

---

## 6. Co oznacza `-f Dockerfile_z_multistage`

Polecenie:

```bash
docker build -f Dockerfile_z_multistage -t fastapi-multistage .
```

oznacza:

* `-f Dockerfile_z_multistage` — użyj wskazanego pliku zamiast domyślnego `Dockerfile`,
* `-t fastapi-multistage` — nadaj nazwę obrazowi,
* `.` — użyj bieżącego katalogu jako kontekstu budowania.

---

## 7. Porównanie obrazów

Po zbudowaniu obu wersji sprawdź listę obrazów:

```bash
docker images
```

Porównaj:

* `fastapi-basic`
* `fastapi-multistage`

Zwróć uwagę na rozmiar i nazwę obrazu.

---

## 8. Zadania do wykonania

### Zadanie 1

Zbuduj i uruchom obraz z pliku `Dockerfile`.

### Zadanie 2

Zbuduj i uruchom obraz z pliku `Dockerfile_z_multistage`.

### Zadanie 3

Sprawdź działanie endpointów:

* `/`
* `/health`

### Zadanie 4

Porównaj obrazy poleceniem:

```bash
docker images
```

### Zadanie 5

Odpowiedz:

* który plik buduje obraz klasyczny?
* który plik buduje obraz multistage?
* po co używamy `COPY --from=builder`?
* dlaczego przy drugim pliku trzeba użyć `-f`?

---

## 9. Pytania do przemyślenia i dyskusji

1. Co robi instrukcja `FROM python:3.12-slim`?
2. Po co ustawiamy `WORKDIR`?
3. Co robi `COPY app ./app`?
4. Do czego służy etap `builder`?
5. Co daje budowanie wieloetapowe?

---

## 10. Na skróty dla niecierpliwych :) 

Wejdź do katalogu projektu:

```bash
cd 3-cwiczenie
```

Zbuduj wersję podstawową:

```bash
docker build -t fastapi-basic .
```

Zbuduj wersję multistage:

```bash
docker build -f Dockerfile_z_multistage -t fastapi-multistage .
```

Uruchom wybrany obraz:

```bash
docker run -p 8000:8000 fastapi-basic
```

albo:

```bash
docker run -p 8000:8000 fastapi-multistage
```
