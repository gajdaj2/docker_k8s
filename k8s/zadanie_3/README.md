# k8s/zadanie_3 - testy integracyjne aplikacji Flask + Redis jako Job

To zadanie rozwija `k8s/zadanie_2`.

Student uruchamia ten sam typ aplikacji:

1. Redis,
2. aplikacje Flask liczaca odwiedziny,
3. `Service` i `Ingress`,
4. a dodatkowo `Job`, ktory uruchamia testy integracyjne wewnatrz klastra Kubernetes.

## Cel zadania

Uruchom w Minikube:

- Redis,
- aplikacje Flask korzystajaca z Redis,
- `Service` dla Redis i Flask,
- `Ingress` dla hosta `flask-redis-tests.local`,
- `Job`, ktory wykona testy integracyjne przeciwko uruchomionej aplikacji.

## Struktura katalogu

```text
k8s/zadanie_3/
├── app/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── tests/
│       └── integration/
│           └── test_endpoints.py
└── manifests/
    ├── flask-deployment.yaml
    ├── flask-service.yaml
    ├── ingress.yaml
    ├── redis-deployment.yaml
    ├── redis-service.yaml
    └── tests-job.yaml
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

## Krok 2. Zbuduj obraz aplikacji razem z testami

Przejdz do katalogu zadania:

```bash
cd k8s/zadanie_3
```

Zbuduj obraz:

```bash
minikube image build -t flask-redis-k8s-tests:1.0 ./app
```

Ten sam obraz bedzie uzyty przez:

- `Deployment` aplikacji Flask,
- `Job` z testami integracyjnymi.

## Krok 3. Uruchom Redis, Flask i Ingress

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
- `Ingress` dla hosta `flask-redis-tests.local`.

## Krok 5. Sprawdz aplikacje recznie

NodePort:

```bash
curl http://$(minikube ip):30081/
curl http://$(minikube ip):30081/health
```

Ingress:

```bash
curl --resolve flask-redis-tests.local:80:$(minikube ip) http://flask-redis-tests.local/
curl --resolve flask-redis-tests.local:80:$(minikube ip) http://flask-redis-tests.local/health
```

## Krok 6. Uruchom testy integracyjne jako Job

Najpierw upewnij sie, ze aplikacja dziala:

```bash
kubectl get pods
```

Nastepnie uruchom Job:

```bash
kubectl delete job flask-tests-zad3 --ignore-not-found
kubectl apply -f manifests/tests-job.yaml
```

## Krok 7. Sprawdz wynik Joba

```bash
kubectl get jobs
kubectl get pods
kubectl wait --for=condition=complete job/flask-tests-zad3 --timeout=120s
kubectl logs job/flask-tests-zad3
```

Jesli testy przejda poprawnie, Job powinien osiagnac status `Complete`.

## Krok 8. Posprzataj po cwiczeniu

```bash
kubectl delete job flask-tests-zad3 --ignore-not-found
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
4. `Ingress` udostepniajacego aplikacje,
5. `Job`, ktory uruchamia testy integracyjne.

Po wykonaniu zadania:

1. sprawdz status Podow, `Service` i `Ingress`,
2. sprawdz aplikacje recznie przez `NodePort` lub `Ingress`,
3. uruchom Job z testami,
4. sprawdz logi Joba,
5. potwierdz, ze Job zakonczyl sie statusem `Complete`.

## Przydatne komendy

```bash
minikube start
minikube addons enable ingress
minikube image build -t flask-redis-k8s-tests:1.0 ./app
kubectl apply -f manifests/redis-deployment.yaml
kubectl apply -f manifests/redis-service.yaml
kubectl apply -f manifests/flask-deployment.yaml
kubectl apply -f manifests/flask-service.yaml
kubectl apply -f manifests/ingress.yaml
kubectl get pods
kubectl get services
kubectl get ingress
curl http://$(minikube ip):30081/
curl http://$(minikube ip):30081/health
curl --resolve flask-redis-tests.local:80:$(minikube ip) http://flask-redis-tests.local/
curl --resolve flask-redis-tests.local:80:$(minikube ip) http://flask-redis-tests.local/health
kubectl delete job flask-tests-zad3 --ignore-not-found
kubectl apply -f manifests/tests-job.yaml
kubectl get jobs
kubectl wait --for=condition=complete job/flask-tests-zad3 --timeout=120s
kubectl logs job/flask-tests-zad3
```
