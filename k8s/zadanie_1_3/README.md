# k8s/zadanie_1_3 - Pod, Deployment, Service i diagnostyka przez kubectl

To zadanie rozwija `zadanie_1_1`.

Student:

1. uruchamia Pod, `Deployment` i `Service`,
2. cwiczy wejscie do kontenera przez `kubectl exec`,
3. analizuje zasoby i logi przez `kubectl`,
4. poznaje dodatkowe przydatne polecenia do codziennej pracy z Kubernetes.

## Cel zadania

Uruchom w Minikube:

- Pod `nginx`,
- `Deployment` `nginx`,
- `Service`, ktory kieruje ruch do Podow z etykieta `app: nginx`.

Nastepnie:

- wejdz do Poda przez `kubectl exec`,
- przeanalizuj logi i konfiguracje zasobow,
- przeprowadz kilka prostych operacji diagnostycznych.

## Struktura katalogu

```text
k8s/zadanie_1_3/
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

## Krok 2. Utworz Pod, Deployment i Service

Przejdz do katalogu zadania:

```bash
cd k8s/zadanie_1_3
```

Uruchom zasoby:

```bash
kubectl apply -f pod.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Sprawdzenie:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get endpoints
```

## Krok 3. Sprawdz zasoby bardziej szczegolowo

```bash
kubectl describe pod nginx-pod
kubectl describe deployment nginx-deployment
kubectl describe service nginx-service
```

To pozwoli zobaczyc:

- status kontenerow,
- liczbe replik,
- selektory i endpointy uslugi,
- zdarzenia zwiazane z zasobami.

## Krok 4. Wejdz do Poda przez `kubectl exec`

Wejdz do prostego Poda:

```bash
kubectl exec -it nginx-pod -- sh
```

Po wejsciu mozesz wykonac:

```bash
ls
hostname
ps
exit
```

Mozesz tez wejsc do jednego z Podow utworzonych przez `Deployment`:

```bash
kubectl exec -it $(kubectl get pod -l source=deployment -o jsonpath='{.items[0].metadata.name}') -- sh
```

## Krok 5. Analizuj logi przez `kubectl`

Logi pojedynczego Poda:

```bash
kubectl logs nginx-pod
```

Logi z Deploymentu:

```bash
kubectl logs deployment/nginx-deployment
```

Sledzenie logow na zywo:

```bash
kubectl logs -f nginx-pod
```

W przypadku `Service` nie ma osobnych logow kontenera, dlatego do analizy uslugi uzywaj:

```bash
kubectl describe service nginx-service
kubectl get endpoints nginx-service
```

## Krok 6. Sprawdz dzialanie uslugi

Uruchom `port-forward`:

```bash
kubectl port-forward svc/nginx-service 8080:80
```

W drugim terminalu sprawdz odpowiedz:

```bash
curl http://127.0.0.1:8080/
```

Powinienes zobaczyc domyslna strone `nginx`.

## Krok 7. Dodatkowe przydatne polecenia do przećwiczenia

Podglad wszystkiego w namespace:

```bash
kubectl get all
kubectl get pods -o wide
```

Podglad definicji YAML:

```bash
kubectl get pod nginx-pod -o yaml
kubectl get deployment nginx-deployment -o yaml
kubectl get service nginx-service -o yaml
```

Sprawdzenie rollout Deploymentu:

```bash
kubectl rollout status deployment/nginx-deployment
```

Skalowanie Deploymentu:

```bash
kubectl scale deployment nginx-deployment --replicas=3
kubectl get pods
```

Powrot do dwoch replik:

```bash
kubectl scale deployment nginx-deployment --replicas=2
```

Podejrzenie zdarzen w klastrze:

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

Test samonaprawy Deploymentu:

```bash
kubectl delete pod -l source=deployment
kubectl get pods -w
```

Po usunieciu Podow Deployment powinien automatycznie utworzyc nowe.

## Krok 8. Posprzataj po cwiczeniu

```bash
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete -f pod.yaml
```

## Zadanie dla studenta

### Zadanie 1

W katalogu `k8s/zadanie_1_3`:

1. uruchom Pod `nginx`,
2. uruchom `Deployment` `nginx`,
3. utworz `Service`,
4. sprawdz endpointy uslugi,
5. wejdz do Poda przez `kubectl exec`,
6. przeanalizuj logi Poda i Deploymentu,
7. przeanalizuj konfiguracje `Service`,
8. wykonaj przynajmniej trzy dodatkowe polecenia diagnostyczne z tego zadania.

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
kubectl exec -it nginx-pod -- sh
kubectl exec -it $(kubectl get pod -l source=deployment -o jsonpath='{.items[0].metadata.name}') -- sh
kubectl logs nginx-pod
kubectl logs deployment/nginx-deployment
kubectl logs -f nginx-pod
kubectl port-forward svc/nginx-service 8080:80
curl http://127.0.0.1:8080/
kubectl get all
kubectl get pods -o wide
kubectl get pod nginx-pod -o yaml
kubectl get deployment nginx-deployment -o yaml
kubectl get service nginx-service -o yaml
kubectl rollout status deployment/nginx-deployment
kubectl scale deployment nginx-deployment --replicas=3
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete -f pod.yaml
```
