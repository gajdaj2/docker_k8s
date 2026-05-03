# 0-cwiczenia - proste budowanie obrazu, uruchomienie kontenera i podlaczenie volumenu

To zadanie pokazuje najprostszy przeplyw pracy z Dockerem:

1. zbudowanie obrazu z aplikacja,
2. uruchomienie kontenera,
3. podlaczenie katalogu jako volumenu,
4. wejscie do kontenera i sprawdzenie, czy volumen jest widoczny.

## Struktura zadania

```text
0-cwiczenia/
├── app/
│   ├── Dockerfile
│   ├── app.py
│   ├── healthcheck.py
│   └── requirements.txt
└── volumen/
    ├── plik.txt
    └── readme.md
```

- `app/` - prosta aplikacja FastAPI uruchamiana w kontenerze na porcie `8080`
- `volumen/` - katalog z plikami, ktory podlaczysz do kontenera

## Krok 1. Przejdz do katalogu zadania

```bash
cd 0-cwiczenia
```

## Krok 2. Zbuduj obraz Docker

```bash
docker build -t lab0-fastapi ./app
```

Opis komendy:

- `docker build` - buduje obraz Docker
- `-t lab0-fastapi` - nadaje obrazowi nazwe `lab0-fastapi`
- `./app` - uzywa katalogu `app` jako kontekstu budowania

## Krok 3. Uruchom kontener bez volumenu

```bash
docker run --rm -d --name lab0-app -p 8080:8080 lab0-fastapi
```

Opis komendy:

- `--rm` - usuwa kontener po zatrzymaniu
- `-d` - uruchamia kontener w tle
- `--name lab0-app` - nadaje kontenerowi czytelna nazwe
- `-p 8080:8080` - mapuje port `8080` kontenera na port `8080` hosta

Sprawdzenie:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
```

Powinienes otrzymac odpowiedzi:

```text
{"Hello":"World"}
```

oraz:

```text
{"status":"ok"}
```

## Krok 4. Zatrzymaj poprzedni kontener

```bash
docker stop lab0-app
```

## Krok 5. Uruchom kontener z podlaczonym volumenem

W tym zadaniu podlaczamy lokalny katalog `0-cwiczenia/volumen` do katalogu `/dane` wewnatrz kontenera.

```bash
docker run --rm -d --name lab0-app -p 8080:8080 -v "$(pwd)/volumen:/dane" lab0-fastapi
```

Opis dodatkowego fragmentu:

- `-v "$(pwd)/volumen:/dane"` - mapuje katalog `volumen` z komputera do katalogu `/dane` w kontenerze

## Krok 6. Wejdz do kontenera

Obraz jest oparty o Alpine, dlatego do srodka wchodzimy przez `sh`, a nie `bash`.

```bash
docker exec -it lab0-app sh
```

## Krok 7. Sprawdz w kontenerze, czy volumen jest podlaczony

Po wejsciu do kontenera wykonaj:

```bash
ls /dane
cat /dane/readme.md
```

Powinienes zobaczyc pliki:

- `plik.txt`
- `readme.md`

Mozesz tez sprawdzic punkt montowania:

```bash
mount | grep /dane
```

Jesli chcesz dodatkowo potwierdzic, ze to ten sam katalog co na hoscie, utworz plik w kontenerze:

```bash
echo "test z kontenera" > /dane/test.txt
exit
```

A potem na komputerze sprawdz:

```bash
cat volumen/test.txt
```

Jesli plik jest widoczny na hoscie, to znaczy, ze volumen dziala poprawnie.

## Krok 8. Posprzataj po cwiczeniu

```bash
docker stop lab0-app
docker image ls
```

Jesli chcesz usunac obraz:

```bash
docker rmi lab0-fastapi
```

## Zadania dla studenta

### Zadanie 1

Zbuduj obraz `lab0-fastapi` z katalogu `app`.

### Zadanie 2

Uruchom kontener i sprawdz endpointy `/` oraz `/health`.

### Zadanie 3

Podlacz katalog `volumen` do kontenera jako `/dane`.

### Zadanie 4

Wejdz do kontenera i sprawdz, czy w `/dane` sa pliki `readme.md` oraz `plik.txt`.

### Zadanie 5

Utworz nowy plik w `/dane` z poziomu kontenera i sprawdz, czy pojawil sie w katalogu `volumen` na hoscie.
