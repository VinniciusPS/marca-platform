# MarcaHub
# Architecture Documentation

## 🧩 Business / System Context
![Business Context](docs/images/architecture/business-context.svg)

---

## 🔄 Core Flows

### Reserva-Pagamento
![Reserva-Pagamento](docs/images/flows/reserva-pagamento-fluxo.svg)

### Analytics
![Analytics](docs/images/flows/analytics-fluxo.svg)
---

## 🧠 Containers / Services
![Containers](docs/images/architecture/containers.svg)

---

## 🚀 Deployment


---

## 🗃️ Data Model


```text
marca-platform/
│
├── docs/
│   ├── adr/
│   ├── diagrams/
│   │   ├── business-context/
│   │   ├── flows/
│   │   ├── use-cases/
│   │   ├── db/
│   │   └── infra/
│   └── api/
│
├── services/
│   ├── reservas/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── pagamentos/
│   ├── analytics/
│   
├── bff/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   └── resources/
│   ├── Dockerfile
│   └── pom.xml
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/          
│   │   └── App.js
│   ├── package.json
│   └── public/
│
├── infra/
│   ├── docker-compose.yml
│   └── README.md
│
├── .github/workflows/
│   ├── build.yml
│   └── deploy.yml
├── .gitignore
└── README.md

