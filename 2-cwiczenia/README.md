# 2-cwiczenia - Flask + Docker

To cwiczenie pokazuje, jak uruchomic prosta aplikacje Flask w kontenerze Docker.

## 1. Zawartosc katalogu

- `app.py` - glowna aplikacja Flask
- `requirements.txt` - zaleznosci Pythona
- `Dockerfile` - definicja obrazu Docker

## 2. Uruchomienie lokalnie (bez Dockera)

> Wymagane: Python 3.10+ i `pip`

```bash
cd 2-cwiczenia
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Aplikacja bedzie dostepna pod adresem:

- http://localhost:5000/
- http://localhost:5000/health

## 3. Uruchomienie w Dockerze

W katalogu `2-cwiczenia` wykonaj:

```bash
docker build -t flask-students-app .
docker run --rm -p 5000:5000 flask-students-app
```

Aplikacja bedzie dostepna pod adresem:

- http://localhost:5000/
- http://localhost:5000/health

## 4. Test endpointow

W nowym terminalu uruchom:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

## 5. Zatrzymanie aplikacji

- Lokalnie: `Ctrl + C`
- W Dockerze: `Ctrl + C`

