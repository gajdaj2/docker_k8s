# k8s/zadanie_1_1 - Pod, Deployment i Service

To zadanie jest naturalnym rozszerzeniem `zadanie_1`.

Student:

1. uruchamia prosty Pod z `nginx`,
2. tworzy `Deployment` z `nginx`,
3. tworzy `Service`, ktory wskazuje na Pod lub Pody z `nginx`,
4. sprawdza, czy usluga poprawnie kieruje ruch do aplikacji.

## Cel zadania

Uruchom w Minikube:

- Pod `nginx`,
- `Deployment` `nginx`,
- `Service`, ktory udostepnia ten Pod wewnatrz klastra.

## Struktura katalogu

```text
k8s/zadanie_1_1/
├── deployment.yaml
├── pod.yaml
└── service.yaml
```

## Wymagania

- zainstalowany `minikube`
- zainstalowany `kubectl`
- dzialajacy klaster Minikube

## Krok 1. Uruchom Minikube

```bash
minikube start
```

Sprawdzenie:

```bash
kubectl get nodes
```

## Krok 2. Utworz Pod z pliku YAML

```bash
cd k8s/zadanie_1_1
kubectl apply -f pod.yaml
```

Sprawdzenie:

```bash
kubectl get pods
kubectl describe pod nginx-pod
```

## Krok 3. Utworz Deployment

```bash
kubectl apply -f deployment.yaml
```

Sprawdzenie:

```bash
kubectl get deployments
kubectl get pods
kubectl describe deployment nginx-deployment
```

Powinienes zobaczyc, ze Deployment zarzadza replikami aplikacji `nginx`.

## Krok 4. Utworz Service

```bash
kubectl apply -f service.yaml
```

Sprawdzenie:

```bash
kubectl get services
kubectl describe service nginx-service
```

## Krok 5. Sprawdz powiazanie Service z Podem lub Podami

```bash
kubectl get endpoints
```

Na liscie endpointow `nginx-service` powinny pojawic sie adresy IP Podow z etykieta `app: nginx` i port `80`.

## Krok 6. Sprawdz dzialanie uslugi

Najprostszy sposob to `port-forward`:

```bash
kubectl port-forward svc/nginx-service 8080:80
```

W drugim terminalu:

```bash
curl http://127.0.0.1:8080/
```

Powinienes zobaczyc domyslna strone startowa `nginx`.

## Krok 7. Posprzataj po cwiczeniu

```bash
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete -f pod.yaml
```

## Zadanie dla studenta

### Zadanie 1

Uruchom w Minikube:

1. prosty Pod `nginx`,
2. `Deployment` z `nginx`,
3. `Service`, ktory kieruje ruch do zasobow z etykieta `app: nginx`.

Po wykonaniu zadania:

1. sprawdz status Poda,
2. sprawdz, czy `Deployment` zostal utworzony i czy uruchomil Pody,
3. sprawdz, czy `Service` zostal utworzony,
4. sprawdz endpointy uslugi,
5. polacz sie z usluga przez `kubectl port-forward`,
6. potwierdz przez `curl`, ze `nginx` odpowiada poprawnie.

## Przydatne komendy

```bash
minikube start
kubectl get nodes
kubectl apply -f pod.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get endpoints
kubectl describe pod nginx-pod
kubectl describe deployment nginx-deployment
kubectl describe service nginx-service
kubectl port-forward svc/nginx-service 8080:80
curl http://127.0.0.1:8080/
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete -f pod.yaml
```
