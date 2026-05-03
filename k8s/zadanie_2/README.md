# k8s/zadanie_2 - Redis + Flask udostepnione przez Ingress

To zadanie pokazuje prosty przeplyw pracy w Kubernetes na Minikube:

1. zbudowanie obrazu lokalnej aplikacji Flask,
2. uruchomienie Redis w Kubernetes,
3. uruchomienie aplikacji Flask polaczonej z Redis,
4. wystawienie aplikacji przez `Service`,
5. udostepnienie jej na zewnatrz przez `Ingress`.

## Cel zadania

Uruchom w Minikube:

- Redis,
- aplikacje Flask liczaca odwiedziny,
- Ingress kierujacy ruch na aplikacje pod adresem `flask-redis.local`.

## Struktura katalogu

```text
k8s/zadanie_2/
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── manifests/
    ├── flask-deployment.yaml
    ├── flask-service.yaml
    ├── ingress.yaml
    ├── redis-deployment.yaml
    └── redis-service.yaml
```

## Wymagania

- dzialajacy `minikube`
- zainstalowany `kubectl`
- wlaczony addon `ingress`

## Krok 1. Uruchom Minikube i Ingress

```bash
minikube start
minikube addons enable ingress
```

Sprawdzenie:

```bash
kubectl get pods -n ingress-nginx
```

## Krok 2. Zbuduj obraz aplikacji w Minikube

Przejdz do katalogu zadania:

```bash
cd k8s/zadanie_2
```

Zbuduj obraz:

```bash
minikube image build -t flask-redis-k8s:1.0 ./app
```

## Krok 3. Uruchom Redis i aplikacje Flask

```bash
kubectl apply -f manifests/redis-deployment.yaml
kubectl apply -f manifests/redis-service.yaml
kubectl apply -f manifests/flask-deployment.yaml
kubectl apply -f manifests/flask-service.yaml
kubectl apply -f manifests/ingress.yaml
```

## Krok 4. Sprawdz zasoby

```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

Powinienes zobaczyc:

- Pod Redis w statusie `Running`,
- Pod aplikacji Flask w statusie `Running`,
- `Service` dla Redis,
- `Service` dla Flask,
- `Ingress` dla hosta `flask-redis.local`.

## Krok 5. Sprawdz dzialanie aplikacji z zewnatrz przez NodePort

Poniewaz `flask-service` ma typ `NodePort`, aplikacja jest dostepna z zewnatrz po adresie Minikube i porcie `30080`.

Pobierz adres IP Minikube:

```bash
minikube ip
```

Nastepnie otworz aplikacje:

```bash
curl http://$(minikube ip):30080/
```

Mozesz tez sprawdzic endpoint health:

```bash
curl http://$(minikube ip):30080/health
```

## Krok 6. Udostepnij aplikacje na zewnatrz w Codespaces

W GitHub Codespaces sam `NodePort` w Minikube zwykle nie wystarcza do publikacji aplikacji poza kontener roboczy. Powod jest prosty: aplikacja nasluchuje na adresie IP Minikube, a nie bezposrednio na porcie kontenera Codespaces.

Z tego powodu trzeba wystawic usluge Kubernetes na lokalny port kontenera przez `kubectl port-forward`.

Uruchom w osobnym terminalu:

```bash
kubectl port-forward --address 0.0.0.0 svc/flask-service 8080:80
```

Po uruchomieniu polecenia aplikacja bedzie dostepna lokalnie pod adresem:

```bash
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/health
```

Wtedy Codespaces wykryje port `8080` jako port nasluchujacy i bedziesz mogl go udostepnic na zewnatrz z zakladki `Ports`.

Jesli chcesz, aby link byl publiczny, ustaw widocznosc portu `8080` na `Public`.

## Krok 7. Sprawdz dzialanie aplikacji przez Ingress

Pobierz adres IP Minikube:

```bash
minikube ip
```

Nastepnie wykonaj:

```bash
curl --resolve flask-redis.local:80:$(minikube ip) http://flask-redis.local/
```

Powinienes zobaczyc strone HTML z informacja:

- ze aplikacja Flask dziala,
- ze polaczenie z Redis jest poprawne,
- ze liczba odwiedzin rosnie przy kolejnych odswiezeniach.

Mozesz tez sprawdzic endpoint health:

```bash
curl --resolve flask-redis.local:80:$(minikube ip) http://flask-redis.local/health
```

## Krok 8. Podejrzyj logi aplikacji

```bash
kubectl logs deployment/flask-app
```

## Krok 9. Posprzataj po cwiczeniu

```bash
kubectl delete -f manifests/ingress.yaml
kubectl delete -f manifests/flask-service.yaml
kubectl delete -f manifests/flask-deployment.yaml
kubectl delete -f manifests/redis-service.yaml
kubectl delete -f manifests/redis-deployment.yaml
```

## Zadanie dla studenta

### Zadanie 1

Uruchom w Minikube prosty zestaw skladajacy sie z:

1. Redis,
2. aplikacji Flask korzystajacej z Redis,
3. `Service` dla aplikacji,
4. `Ingress`, ktory udostepnia aplikacje pod adresem `flask-redis.local`.

Po wykonaniu zadania:

1. sprawdz status Podow,
2. sprawdz status `Service` i `Ingress`,
3. wejdz na aplikacje przez `NodePort`,
4. wystaw aplikacje w Codespaces przez `kubectl port-forward`,
5. wejdz na aplikacje przez `curl --resolve`,
6. sprawdz endpoint `/health`,
7. potwierdz, ze licznik odwiedzin rosnie po kolejnych wywolaniach.

## Przydatne komendy

```bash
minikube start
minikube addons enable ingress
minikube image build -t flask-redis-k8s:1.0 ./app
kubectl apply -f manifests/redis-deployment.yaml
kubectl apply -f manifests/redis-service.yaml
kubectl apply -f manifests/flask-deployment.yaml
kubectl apply -f manifests/flask-service.yaml
kubectl apply -f manifests/ingress.yaml
kubectl get pods
kubectl get services
kubectl get ingress
kubectl logs deployment/flask-app
curl http://$(minikube ip):30080/
curl http://$(minikube ip):30080/health
kubectl port-forward --address 0.0.0.0 svc/flask-service 8080:80
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/health
curl --resolve flask-redis.local:80:$(minikube ip) http://flask-redis.local/
curl --resolve flask-redis.local:80:$(minikube ip) http://flask-redis.local/health
```
