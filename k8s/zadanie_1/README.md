# k8s/zadanie_1 - uruchom swoj pierwszy Pod na Minikube

To zadanie pokazuje najprostszy start z Kubernetes:

1. uruchomienie klastra Minikube,
2. stworzenie pierwszego Poda poleceniem `kubectl run`,
3. stworzenie tego samego typu Poda z pliku YAML,
4. sprawdzenie, czy Pod dziala,
5. usuniecie Poda po zakonczeniu cwiczenia.

## Cel zadania

Uruchom swoj pierwszy Pod w Minikube przy uzyciu obrazu `nginx` najpierw poleceniem, a potem z pliku YAML.

## Wymagania

- zainstalowany `minikube`
- zainstalowany `kubectl`
- dzialajacy Docker lub inny wspierany driver Minikube

## Krok 1. Uruchom Minikube

```bash
minikube start
```

Sprawdzenie:

```bash
kubectl get nodes
```

Powinienes zobaczyc jeden node w statusie `Ready`.

## Czesc 1. Utworzenie Poda poleceniem `kubectl run`

## Krok 2. Uruchom swoj pierwszy Pod poleceniem

```bash
kubectl run moj-pierwszy-pod --image=nginx
```

## Krok 3. Sprawdz, czy Pod dziala

```bash
kubectl get pods
```

Po chwili status Poda powinien zmienic sie na:

```text
Running
```

Mozesz tez zobaczyc szczegoly:

```bash
kubectl describe pod moj-pierwszy-pod
```

## Krok 4. Sprawdz logi Poda

```bash
kubectl logs moj-pierwszy-pod
```

## Krok 5. Usun Poda utworzonego poleceniem

```bash
kubectl delete pod moj-pierwszy-pod
```

## Czesc 2. Utworzenie Poda z pliku YAML

## Krok 6. Przygotuj plik YAML z definicja Poda

W katalogu `k8s/zadanie_1` znajduje sie przygotowany plik:

```text
pod.yaml
```

Zawiera on definicje Poda `moj-pierwszy-pod` z obrazem `nginx`.

## Krok 7. Uruchom swoj pierwszy Pod z pliku YAML

Stworz Poda poleceniem:

```bash
kubectl apply -f pod.yaml
```

## Krok 8. Sprawdz, czy Pod dziala

```bash
kubectl get pods
```

Po chwili status Poda powinien zmienic sie na:

```text
Running
```

Mozesz tez zobaczyc szczegoly:

```bash
kubectl describe pod moj-pierwszy-pod
```

Mozesz tez podejrzec definicje, z ktorej zostal utworzony:

```bash
kubectl get pod moj-pierwszy-pod -o yaml
```

## Krok 9. Sprawdz logi Poda

```bash
kubectl logs moj-pierwszy-pod
```

## Krok 10. Usun Pod po zakonczeniu cwiczenia

```bash
kubectl delete -f pod.yaml
```

Sprawdzenie:

```bash
kubectl get pods
```

Lista nie powinna juz zawierac Poda `moj-pierwszy-pod`.

## Zadanie dla studenta

### Zadanie 1

Uruchom Minikube i stworz swoj pierwszy Pod o nazwie `moj-pierwszy-pod` z obrazu `nginx` na dwa sposoby:

1. najpierw poleceniem `kubectl run`,
2. potem z pliku `pod.yaml`.

Nastepnie:

1. sprawdz, czy node ma status `Ready`,
2. sprawdz, czy pierwszy Pod ma status `Running`,
3. wyswietl szczegoly i logi pierwszego Poda,
4. usun pierwszego Poda,
5. utworz drugiego Poda z pliku `pod.yaml`,
6. wyswietl definicje Poda w YAML,
7. usun Pod po zakonczeniu pracy.

## Przydatne komendy

```bash
minikube start
kubectl get nodes
kubectl run moj-pierwszy-pod --image=nginx
kubectl get pods
kubectl describe pod moj-pierwszy-pod
kubectl logs moj-pierwszy-pod
kubectl delete pod moj-pierwszy-pod
kubectl apply -f pod.yaml
kubectl get pods
kubectl describe pod moj-pierwszy-pod
kubectl get pod moj-pierwszy-pod -o yaml
kubectl logs moj-pierwszy-pod
kubectl delete -f pod.yaml
```
