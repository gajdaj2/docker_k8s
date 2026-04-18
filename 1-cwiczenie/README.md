# 1-cwiczenie - Node.js + Docker

To cwiczenie pokazuje, jak uruchomic bardzo prosta aplikacje Node.js lokalnie oraz w kontenerze Docker.

## 1. Zawartosc katalogu

- `app.js` - prosta aplikacja HTTP w Node.js
- `package.json` - konfiguracja projektu i skrypt `start`
- `Dockerfile` - definicja obrazu Docker

## 2. Co robi aplikacja

Aplikacja uruchamia serwer HTTP na porcie `3000` i po wejsciu na strone zwraca tekst:

```text
Hello from Docker!
```

Po starcie w terminalu powinien pojawic sie komunikat:

```text
Serwer działa na porcie 3000
```

## 3. Uruchomienie lokalnie (bez Dockera)

> Wymagane: Node.js 20+ i `npm`

W katalogu `1-cwiczenie` wykonaj:

```bash
cd 1-cwiczenie
npm install
npm start
```

- `cd 1-cwiczenie` - przechodzi do katalogu z pierwszym cwiczeniem
- `npm install` - instaluje zaleznosci zdefiniowane w `package.json`
- `npm start` - uruchamia aplikacje zgodnie ze skryptem `start`

Aplikacja bedzie dostepna pod adresem:

- http://localhost:3000/

## 4. Sprawdzenie dzialania aplikacji

W nowym terminalu uruchom:

```bash
curl http://localhost:3000/
```

- `curl http://localhost:3000/` - wysyla zapytanie HTTP do lokalnej aplikacji i pokazuje odpowiedz w terminalu

Powinienes otrzymac odpowiedz:

```text
Hello from Docker!
```

## 5. Uruchomienie w Dockerze

W katalogu `1-cwiczenie` wykonaj:

```bash
docker build -t node-basic .
docker run --rm -p 3000:3000 node-basic
```

- `docker build -t node-basic .` - buduje obraz Docker z biezacego katalogu i nadaje mu nazwe `node-basic`
- `docker run --rm -p 3000:3000 node-basic` - uruchamia kontener z obrazu `node-basic`, mapuje port 3000 z kontenera na port 3000 hosta i usuwa kontener po zatrzymaniu

Aplikacja bedzie dostepna pod adresem:

- http://localhost:3000/

## 6. Sprawdzenie aplikacji w kontenerze

W nowym terminalu uruchom:

```bash
curl http://localhost:3000/
```

- `curl http://localhost:3000/` - sprawdza, czy aplikacja uruchomiona w kontenerze odpowiada poprawnie

Jesli wszystko dziala poprawnie, zobaczysz:

```text
Hello from Docker!
```

## 7. Omowienie pliku `Dockerfile`

Plik `Dockerfile`:

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

Znaczenie najwazniejszych instrukcji:

- `FROM node:20-alpine` - uzywa lekkiego obrazu z Node.js 20
- `WORKDIR /app` - ustawia katalog roboczy w kontenerze
- `COPY package*.json ./` - kopiuje pliki konfiguracyjne npm
- `RUN npm install` - instaluje zaleznosci projektu
- `COPY . .` - kopiuje pozostale pliki aplikacji
- `EXPOSE 3000` - informuje, ze aplikacja nasluchuje na porcie 3000
- `CMD ["npm", "start"]` - uruchamia aplikacje po starcie kontenera

## 8. Zadania do wykonania

### Zadanie 1

Uruchom aplikacje lokalnie przez `npm start`.

**Rozwiazanie:**

```bash
cd 1-cwiczenie
npm install
npm start
```

- `cd 1-cwiczenie` - przechodzi do katalogu z zadaniem
- `npm install` - instaluje zaleznosci potrzebne do uruchomienia aplikacji
- `npm start` - startuje serwer HTTP na porcie 3000

### Zadanie 2

Sprawdz jej dzialanie poleceniem:

```bash
curl http://localhost:3000/
```

**Rozwiazanie:**

Po uruchomieniu aplikacji polecenie:

```bash
curl http://localhost:3000/
```

Opis komendy:

- `curl http://localhost:3000/` - wysyla zapytanie do uruchomionej aplikacji i wypisuje odpowiedz

powinno zwrocic:

```text
Hello from Docker!
```

### Zadanie 3

Zbuduj obraz Docker na podstawie `Dockerfile`.

**Rozwiazanie:**

```bash
cd 1-cwiczenie
docker build -t node-basic .
```

- `cd 1-cwiczenie` - przechodzi do katalogu zawierajacego `Dockerfile`
- `docker build -t node-basic .` - tworzy obraz Docker o nazwie `node-basic` na podstawie plikow z biezacego katalogu

### Zadanie 4

Uruchom kontener i sprawdz, czy aplikacja odpowiada na porcie `3000`.

**Rozwiazanie:**

```bash
docker run --rm -p 3000:3000 node-basic
```

- `docker run --rm -p 3000:3000 node-basic` - uruchamia kontener z obrazu `node-basic` i udostepnia aplikacje pod `http://localhost:3000`

W drugim terminalu:

```bash
curl http://localhost:3000/
```

- `curl http://localhost:3000/` - sprawdza, czy kontener odpowiada na zapytanie HTTP

Odpowiedz:

```text
Hello from Docker!
```

### Zadanie 5

Zmien tekst odpowiedzi w pliku `app.js`, przebuduj obraz i sprawdz, czy zmiana jest widoczna po uruchomieniu kontenera.

**Rozwiazanie:**

Przykladowa zmiana w `app.js`:

```javascript
const http = require("http");

const server = http.createServer((req, res) => {
  res.end("Nowa odpowiedz z kontenera!");
});

server.listen(3000, () => {
  console.log("Serwer działa na porcie 3000");
});
```

Nastepnie przebuduj obraz i uruchom kontener ponownie:

```bash
docker build -t node-basic .
docker run --rm -p 3000:3000 node-basic
```

- `docker build -t node-basic .` - buduje nowa wersje obrazu z uwzglednieniem zmian w `app.js`
- `docker run --rm -p 3000:3000 node-basic` - uruchamia kontener z przebudowanego obrazu

Sprawdzenie:

```bash
curl http://localhost:3000/
```

- `curl http://localhost:3000/` - pozwala potwierdzic, ze nowy tekst odpowiedzi jest juz widoczny

Nowa odpowiedz powinna byc widoczna w terminalu:

```text
Nowa odpowiedz z kontenera!
```

## 9. Pytania kontrolne

1. Do czego sluzy instrukcja `FROM` w pliku `Dockerfile`?
2. Po co kopiujemy `package.json` przed `COPY . .`?
3. Co robi instrukcja `EXPOSE 3000`?
4. Jaka jest roznica miedzy `docker build` i `docker run`?
5. Dlaczego w poleceniu `docker run` uzywamy `-p 3000:3000`?

## 10. Zatrzymanie aplikacji

- Lokalnie: `Ctrl + C`
- W Dockerze: `Ctrl + C`
