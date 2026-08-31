
[English](README.md) | [Português](README.pt-BR.md)

# Marca Platform

Plataforma de gestão integrada para operações de clínica/serviços, combinando agendamento, processamento de pagamentos e analytics operacional.

## Visão Geral

Marca Platform é um sistema orientado a domínios que permite que empresas gerenciem:

- **Reservas de Serviços** — Agendamento, disponibilidade e confirmação de consultas/serviços
- **Processamento de Pagamentos** — Autorização, processamento e reconciliação de transações
- **Analytics Operacional** — Métricas de negócio, tendências de mercado e decisões estratégicas

O sistema é organizado como uma arquitetura de microsserviços com separação clara de responsabilidades, comunicação assíncrona e uma camada de dados analítica isolada.

## Primeiros Passos

### Para desenvolvedores iniciando o projeto

1. Comece lendo a documentação arquitetural:
   - [`docs/architecture/context.md`](docs/architecture/context.md) — Entenda o contexto geral
   - [`docs/architecture/containers.md`](docs/architecture/containers.md) — Veja os componentes principais

2. Consulte os diagramas para visualizar fluxos:
   - [`docs/diagrams/context.md`](docs/diagrams/context.md) — Diagrama de contexto
   - [`docs/diagrams/flow-booking-payments.md`](docs/diagrams/flow-booking-payments.md) — Fluxo principal

3. Entenda as decisões arquiteturais:
   - [`docs/decisions/adr-002-bff-pattern.md`](docs/decisions/adr-002-bff-pattern.md) — Por que BFF?
   - [`docs/decisions/adr-001-separate-booking-and-payments-apis.md`](docs/decisions/adr-001-separate-booking-and-payments-apis.md) — Por que APIs separadas?

4. Revise o estado atual de implementação:
   - [`docs/deployment/current.md`](docs/deployment/current.md) — O que está implementado

5. Veja a aplicação ao vivo em: 
   - Link: https://marca-platform.vercel.app/

## Estrutura do Repositório

```
.
├── docs/                          # Documentação arquitetural
│   ├── README.md                  # Guia de leitura da documentação
│   ├── architecture/              # Definições conceituais (C4 Model)
│   ├── decisions/                 # Decisões arquiteturais (ADR)
│   ├── deployment/                # Estado de implementação atual
│   ├── diagrams/                  # Diagramas como código (Mermaid)
│   ├── issues/                    # Planejamento e state de evolução
│   └── requirements/              # Especificações funcionais e não-funcionais
│
├── services/                      # Serviços backend
│   ├── api/
│   │   ├── booking/               # API de Reservas
│   │   ├── payments/              # API de Pagamentos
│   │   └── analytics/             # API de Analytics
│   └── bff/                       # Backend-for-Frontend
│
├── view/                          # Frontend Web
│   └── src/                       # React/Vite/Tailwind
│
├── etl/                           # Orquestração e transformação de dados
│   ├── airflow/                   # DAGs de extração
│   └── dbt/                       # Modelos de transformação
│
├── database/                      # Esquemas e migrações
│   └── migrations/                # Flyway migrations
│
├── deploy/                        # Configurações de deployment
│   ├── dev/                       # Ambiente de desenvolvimento
│   └── prd/                       # Ambiente de produção
│
└── scripts/                       # Utilitários e automação
```

## Arquitetura

### Modelo Conceitual

A plataforma segue o **C4 Model** para documentação de arquitetura:

- **Contexto** — Atores, sistemas externos e limites
- **Containers** — Componentes executáveis (serviços, bancos, frontends)
- **Componentes** — Decomposição interna de containers
- **Código** — Implementação

Documentação detalhada: [`docs/README.md`](docs/README.md)

### Padrões Arquiteturais

#### Backend-for-Frontend (BFF)
O BFF orquestra as chamadas para os serviços de domínio, fornecendo uma interface otimizada para o frontend.

- **Decisão**: [`adr-002-bff-pattern.md`](docs/decisions/adr-002-bff-pattern.md)

#### Separação de Domínios
Reservas e Pagamentos são APIs independentes com:
- Bancos de dados próprios
- Ciclos de deploy desacoplados
- Contratos bem definidos

- **Decisão**: [`adr-001-separate-booking-and-payments-apis.md`](docs/decisions/adr-001-separate-booking-and-payments-apis.md)

#### Comunicação Assíncrona
Serviços se comunicam através de um Event Bus para reduzir acoplamento.

- **Decisão**: [`adr-003-event-bus-pattern.md`](docs/decisions/adr-003-event-bus-pattern.md)

#### Analytics Isolado
Banco de dados analítico separado, alimentado por ETL, para OLAP e decisões.

- **Decisão**: [`adr-004-analytics-db.md`](docs/decisions/adr-004-analytics-db.md)

## Dados

### Banco de Dados Principal
PostgreSQL com múltiplos schemas:

- **clinic** — Pacientes, profissionais, agendas
- **operations** — Contratos e operações
- **marketing** — Termos de tendência e estratégia
- **staging** — Dados brutos do ETL
- **silver/gold** — Modelos enriquecidos para analytics
- **control** — Auditoria de cargas

### Pipeline de Dados
1. **Extração** — Airflow extrai dados de fontes (e.g., Google Trends)
2. **Staging** — Dados brutos persistidos em PostgreSQL
3. **Transformação** — dbt transforma em modelos silver/gold
4. **Consumo** — API de Analytics expõe dados via REST

## Componentes Principais

### Frontend (`view/`)
- React + Vite + Tailwind
- Testes com Vitest
- Linting com ESLint

**Status**: Funcional

### BFF (`services/bff/`)
- Java + SpringBoot
- Orquestra serviços de domínio

**Status**: Estrutura inicial, implementação em progresso

### API de Reservas (`services/api/booking/`)
- Python + FastAPI (planejado)

**Status**: Estrutura de arquitetura, sem implementação funcional

### API de Pagamentos (`services/api/payments/`)
- Python + FastAPI (planejado)
- Integração com gateway externo

**Status**: Ponto de entrada mínimo

### API de Analytics (`services/api/analytics/`)
- Python + FastAPI + SQLAlchemy
- Acesso a dados de silver/gold

**Status**: Funcional

### ETL (`etl/`)
- Airflow para orquestração
- dbt para transformação
- Google Trends como fonte

**Status**: Funcional

## Fluxos Principais

### Criação de Reserva e Pagamento

```
1. Operador cria reserva no frontend
2. BFF recebe e encaminha para API de Reservas
3. API de Reservas persiste em PENDING_PAYMENT
4. Evento ReservaCriada é publicado no Event Bus
5. API de Pagamentos processa pagamento com gateway
6. Resultado é publicado (confirmado ou recusado)
7. API de Reservas atualiza status da reserva
8. Frontend reflete o novo estado
```

Diagrama detalhado: [`docs/diagrams/flow-booking-payments.md`](docs/diagrams/flow-booking-payments.md)

### Analytics

```
1. Airflow extrai Google Trends diariamente
2. Dados brutos são persistidos em staging
3. dbt transforma em modelos silver/gold
4. API de Analytics expõe dados via endpoints REST
5. Frontend ou ferramentas externas consultam a API
```

Diagrama detalhado: [`docs/diagrams/flow-analytics.md`](docs/diagrams/flow-analytics.md)

## Decisões Importantes

Todas as decisões arquiteturais relevantes foram documentadas como ADRs:

| ADR | Decisão | Status |
|-----|---------|--------|
| [001](docs/decisions/adr-001-separate-booking-and-payments-apis.md) | Separação de Reservas e Pagamentos em APIs distintas | Aceita |
| [002](docs/decisions/adr-002-bff-pattern.md) | Adoção de Backend-for-Frontend | Aceita |
| [003](docs/decisions/adr-003-event-bus-pattern.md) | Comunicação assíncrona via Event Bus | Aceita |
| [004](docs/decisions/adr-004-analytics-db.md) | Banco de dados analítico separado | Aceita |

Leia as justificativas completas em [`docs/decisions/`](docs/decisions/).

## Estado Atual

A implementação está em evolução:

- ✅ **Funcional**: Frontend, Analytics API, ETL
- 🚧 **Parcial**: BFF, API de Pagamentos
- ❌ **Não iniciado**: API de Reservas, Event Bus

Detalhes completos em [`docs/deployment/current.md`](docs/deployment/current.md) e [`docs/issues/Master-plan.md`](docs/issues/Master-plan.md).

## Próximos Passos

1. **Implementar API de Reservas** — Core da funcionalidade de agendamento
2. **Completar fluxo de Pagamentos** — Integração com gateway externo
3. **Implementar Event Bus** — Comunicação assíncrona entre serviços
4. **Adicionar testes E2E** — Validar fluxos principais
5. **Documentar deployment final** — CI/CD para produção

Confira o plano detalhado em [`docs/issues/Master-plan.md`](docs/issues/Master-plan.md).

## Documentação

- **[Guia de Documentação](docs/README.md)** — Como navegar e evoluir a documentação
- **[Arquitetura](docs/architecture/)** — Modelo conceitual (C4)
- **[Decisões](docs/decisions/)** — ADRs justificando escolhas
- **[Deployment](docs/deployment/)** — Estado e estratégia de implementação
- **[Diagramas](docs/diagrams/)** — Fluxos e topologia visual
- **[Issues de Evolução](docs/issues/)** — Planejamento e state de mudanças

## Governança

Este repositório segue a metodologia **Spec-Driven Development (SDD)** com **Harness Engineering** para garantir que mudanças sejam:

- Especificadas explicitamente
- Rastreáveis a requisitos
- Verificáveis através de testes
- Documentadas para continuidade

Consulte [`AGENTS.md`](AGENTS.md) para os princípios de operação.

## Convenções

- Documentação em português do Brasil (pt-BR)
- Código em inglês
- Diagramas como código (Mermaid)
- Decisões formalizadas como ADRs
- Especificações antes da implementação

---

**Última atualização**: 2026-08-30  
**Status**: Arquitetura documentada, implementação em progresso