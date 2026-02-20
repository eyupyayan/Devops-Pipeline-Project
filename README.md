# Task API – End-to-End DevOps læringsprosjekt (lokalt)

Dette prosjektet er et **ende-til-ende DevOps-læringsprosjekt** som kjører **100 % lokalt** med Docker Desktop og Kubernetes.
Målet er å lære samspillet mellom:

* Docker
* Kubernetes
* Helm
* ArgoCD (GitOps)
* Prometheus
* Grafana

uten å bruke cloud-spesifikke tjenester eller overkomplisert sikkerhet.

Prosjektet er bygget stegvis med fokus på **forståelse, verifisering og gode DevOps-vaner**, ikke produksjonsperfeksjon.

---

## Arkitektur – høyt nivå

```text
┌────────────┐
│   GitHub   │
│ (Helm +   │
│  ArgoCD)  │
└─────┬──────┘
      │ GitOps
┌─────▼────────┐
│   ArgoCD     │
│ (argocd ns) │
└─────┬────────┘
      │ Helm render
┌─────▼─────────────────────┐
│ Kubernetes (Docker Desktop)│
│                             │
│  app-dev namespace          │
│   └─ task-api (FastAPI)     │
│                             │
│  app-prod namespace         │
│   └─ task-api (FastAPI)     │
│                             │
│  monitor namespace          │
│   ├─ Prometheus             │
│   └─ Grafana                │
└─────────────────────────────┘
```

---

## Innhold i prosjektet

### Fase 1 – App + Container

* Python FastAPI-applikasjon (flere filer)
* Health endpoint (`/health`)
* Metrics endpoint (`/metrics`)
* Dockerfile
* Bygging og testing av image lokalt
* Push til DockerHub
* Verifisering ved å kjøre imaget etter pull

### Fase 2 – Kubernetes + Helm + ArgoCD

* Helm chart for appen
* Deployment, Service, ConfigMap og HPA
* `values-dev.yaml` og `values-prod.yaml`
* Separate namespaces:

  * `app-dev`
  * `app-prod`
* To Helm releases:

  * `task-api-dev`
  * `task-api-prod`
* ArgoCD installert i `argocd` namespace
* Full GitOps-flyt (ingen manuell `helm install`)

### Fase 3 – Monitoring

* `monitor` namespace
* Prometheus installert og scraping app-metrics
* Grafana installert
* Enkelt dashboard for:

  * request count
  * latency
  * pod CPU-bruk

---

## Repository-struktur

```text
.
├── app/                     # Python FastAPI app
│   ├── main.py
│   ├── api.py
│   ├── models.py
│   ├── storage.py
│   └── metrics.py
├── tests/
│   └── test_health.py
├── Dockerfile
├── requirements.txt
├── .dockerignore
│
├── task-api/                # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── configmap.yaml
│       └── hpa.yaml
│
├── argocd/
│   ├── app-dev.yaml
│   └── app-prod.yaml
│
└── README.md
```

---

## Forutsetninger

Du trenger følgende installert lokalt:

* Docker Desktop (med Kubernetes aktivert)
* kubectl
* helm
* git

Bekreft at Kubernetes kjører:

```bash
kubectl get nodes
```

---

## Kjøre prosjektet lokalt (kortversjon)

### 1. Bygg og push Docker-image

```bash
docker build -t <dockerhub-user>/task-api:1.0.0 .
docker push <dockerhub-user>/task-api:1.0.0
```

---

### 2. Installer ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Port-forward UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

---

### 3. Deploy app via GitOps

```bash
kubectl create namespace app-dev
kubectl create namespace app-prod

kubectl apply -f argocd/app-dev.yaml
kubectl apply -f argocd/app-prod.yaml
```

ArgoCD vil nå:

* hente Helm chart fra Git
* rendere templates
* deploye appen automatisk

---

### 4. Verifiser applikasjonen

```bash
kubectl get pods -n app-dev
kubectl port-forward svc/task-api 8000:8000 -n app-dev
curl http://localhost:8000/health
```

---

### 5. Monitoring

Namespaces:

```bash
kubectl get ns monitor
```

Grafana (eksempel):

```bash
kubectl port-forward svc/grafana 3000:3000 -n monitor
```

Prometheus scraper:

* `/metrics` endpoint fra FastAPI-appen

---

## Viktige prinsipper i prosjektet

* **Én Helm chart – flere miljøer**
* **Ingen manuelle deploys etter GitOps**
* **All konfig via values.yaml**
* **Testing før container**
* **Observability bygget inn tidlig**
* **Alt kjører lokalt**

---

## Hva dette prosjektet bevisst ikke gjør

* Ingen cloud-leverandører
* Ingen ingress eller TLS
* Ingen secrets-manager
* Ingen CI-pipeline (kan legges til senere)
* Ingen Kustomize (kun Helm)

---

## Videre forbedringer (frivillig)

* Legge til CI (GitHub Actions)
* Bytte in-memory storage med database
* Legge til readiness/liveness probes
* Lage flere Grafana dashboards
* Canary-deploy via Argo Rollouts

---

## Mål med prosjektet

Dette repoet er laget for å:

* lære DevOps-fundamentet i praksis
* forstå **hvorfor** ting gjøres, ikke bare **hvordan**
* gi et solid grunnlag før cloud og enterprise-oppsett

---

Hvis du vil, Batman, kan jeg:

* kode-review Helm chartet
* “late som” dette er en jobbintervju-case
* utvide med CI i samme læringsstil
