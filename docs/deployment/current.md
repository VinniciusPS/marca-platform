# Deployment Atual

Estado real de implementação do sistema conforme documentado em `docs/issues/Master-plan.md`.

## Topologia de Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    Aplicação Web                             │
│                   (React/Vite/Tailwind)                      │
│                       view/src                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend-for-Frontend (BFF)                      │
│                 (Java/SpringBoot)                            │
│               services/bff [parcial]                         │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌────────┐      ┌─────────┐      ┌──────────┐
    │Reservas│      │Pagamentos│     │ Analytics│
    │  API   │      │   API    │     │   API    │
    │[vazio] │      │[mínima]  │     │[funcional]
    └────┬───┘      └────┬─────┘     └────┬─────┘
         │                │                 │
         ▼                ▼                 │
    ┌────────┐      ┌─────────┐            │
    │ Reservas       │Pagamentos          │
    │  Schema        │ Schema             │
    │ (clinic)       │(operations)        │
    └────────┘      └─────────┘            │
         │                │                │
         └────────┬───────┘                │
                  │                        │
         [Event Bus - planejado]           │
                  │                        │
                  ├────────────────────────┤
                  │                        │
                  ▼                        ▼
            ┌──────────┐           ┌──────────────┐
            │Analytics │           │Analytics DB  │
            │ Jobs     │           │   (OLAP)     │
            │(Airflow) │           │ (silver/gold)│
            └────┬─────┘           └──────────────┘
                 │
                 ▼
            ┌──────────────┐
            │ PostgreSQL   │
            │   Central    │
            │ (Staging)    │
            └──────────────┘
```

## Componentes Implementados

### Frontend
- **Localização**: `view/`
- **Tecnologia**: React, Vite, Tailwind
- **Status**: Funcional
- **Recursos**: Scripts de build/test com vitest e ESLint

### BFF (Backend-for-Frontend)
- **Localização**: `services/bff/`
- **Tecnologia**: Java, SpringBoot
- **Status**: Estrutura inicial, sem implementação funcional
- **Responsabilidade**: Orquestração de chamadas para serviços de domínio

### API de Reservas
- **Localização**: `services/api/booking/`
- **Status**: Apenas estrutura planejada, sem implementação
- **Responsabilidade**: Gerenciar ciclo de vida de reservas

### API de Pagamentos
- **Localização**: `services/api/payments/`
- **Status**: Ponto de entrada mínimo, sem fluxo completo
- **Responsabilidade**: Processar pagamentos e integrar com gateway externo

### API de Analytics
- **Localização**: `services/api/analytics/`
- **Tecnologia**: Python, FastAPI, SQLAlchemy
- **Status**: Funcional
- **Recursos**: 
  - Rotas de pacientes
  - Endpoints de analytics
  - Acesso a dados via ORM

### ETL e Transformação
- **Localização**: `etl/airflow/` e `etl/dbt/google_trends/`
- **Status**: Funcional
- **Responsabilidades**:
  - Extração de Google Trends via `pytrends`
  - Persistência em `staging.stg_google_trends`
  - Transformação em modelos `silver` e `gold`

## Banco de Dados

### PostgreSQL Central
- **Host**: Render (produção)
- **Schemas**:
  - `clinic` — Pacientes, profissionais, agendas, serviços
  - `operations` — Contratos profissionais
  - `marketing` — Termos e benchmarks de marketing
  - `staging` — Dados brutos de carga ETL
  - `silver` — Modelos enriquecidos
  - `gold` — Visões analíticas consumidas pela API
  - `control` — Histórico de cargas ETL

### Migrações
- **Localização**: `database/render/migrations/`
- **Ferramenta**: Flyway
- **CI/CD**: Workflow GitHub Actions (`.github/workflows/`)

## Integrações Externas

### Google Trends
- **Ferramenta**: `pytrends`
- **Uso**: Extração de termos de tendência para análise de marketing
- **Pipeline**: Airflow → PostgreSQL (staging) → dbt → Analytics

### Gateway de Pagamento
- **Status**: Documentado em arquitetura, sem implementação concreta neste snapshot
- **Responsabilidade**: Processar pagamentos (será integrado via API de Pagamentos)

## Infraestrutura de Deployment

### Desenvolvimento
- **Localização**: `deploy/dev/database/`
- **Características**: Configurações de desenvolvimento local

### Produção
- **Localização**: `deploy/prd/`
- **Database**: Render (PostgreSQL gerenciado)
- **CI/CD**: GitHub Actions

## Gaps Identificados

### Não Implementado
1. Event Bus — Documentado em ADR-003, não implementado
2. Integração entre APIs — BFF não orquestra completamente
3. Reservas API — Apenas estrutura
4. Pagamentos completo — Sem fluxo de pagamento real
5. Testes automatizados — Não evidentes para backend

### Discrepâncias
- Arquitetura documentada (ideal) vs. implementação (parcial)
- Analytics é o componente mais maduro
- Serviços de negócio (reservas, pagamentos) são os menos desenvolvidos

## Próximos Passos Recomendados

Conforme `docs/issues/Master-plan.md`:

1. Completar implementação de Reservas API
2. Implementar fluxo de Pagamentos com gateway
3. Implementar Event Bus para comunicação assíncrona
4. Finalizar integração de BFF
5. Adicionar suítes de teste end-to-end

## Referências

- `docs/issues/Master-plan.md` — Estado observado completo
- `docs/architecture/containers.md` — Topologia arquitetural
- `docs/decisions/adr-002-bff-pattern.md` — Justificativa de BFF
- `docs/decisions/adr-003-event-bus-pattern.md` — Justificativa de Event Bus
