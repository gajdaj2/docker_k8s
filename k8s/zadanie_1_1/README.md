# k8s/zadanie_1_1 - Pod i Service

To zadanie jest naturalnym rozszerzeniem `zadanie_1`.

Student:

1. uruchamia prosty Pod z `nginx`,
2. tworzy `Service`, ktory wskazuje na ten Pod,
3. sprawdza, czy usluga poprawnie kieruje ruch do aplikacji.

## Cel zadania

Uruchom w Minikube:

- Pod `nginx`,
- `Service`, ktory udostepnia ten Pod wewnatrz klastra.

## Struktura katalogu

```text
k8s/zadanie_1_1/
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

## Krok 3. Utworz Service

```bash
kubectl apply -f service.yaml
```

Sprawdzenie:

```bash
kubectl get services
kubectl describe service nginx-service
```

## Krok 4. Sprawdz powiazanie Service z Podem

```bash
kubectl get endpoints
```

Na liscie endpointow `nginx-service` powinien wskazywac na adres IP Poda i port `80`.

## Krok 5. Sprawdz dzialanie uslugi

Najprostszy sposob to `port-forward`:

```bash
kubectl port-forward svc/nginx-service 8080:80
```

W drugim terminalu:

```bash
curl http://127.0.0.1:8080/
```

Powinienes zobaczyc domyslna strone startowa `nginx`.

## Krok 6. Posprzataj po cwiczeniu

```bash
kubectl delete -f service.yaml
kubectl delete -f pod.yaml
```

## Zadanie dla studenta

### Zadanie 1

Uruchom w Minikube prosty Pod `nginx` i dodaj do niego `Service`.

Po wykonaniu zadania:

1. sprawdz status Poda,
2. sprawdz, czy `Service` zostal utworzony,
3. sprawdz endpointy uslugi,
4. polacz sie z usluga przez `kubectl port-forward`,
5. potwierdz przez `curl`, ze `nginx` odpowiada poprawnie.

## Przydatne komendy

```bash
minikube start
kubectl get nodes
kubectl apply -f pod.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get services
kubectl get endpoints
kubectl describe pod nginx-pod
kubectl describe service nginx-service
kubectl port-forward svc/nginx-service 8080:80
curl http://127.0.0.1:8080/
kubectl delete -f service.yaml
kubectl delete -f pod.yaml
```
