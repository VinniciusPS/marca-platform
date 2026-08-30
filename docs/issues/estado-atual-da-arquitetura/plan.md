# Plano de Implementação — P1

## 1. Referências

* Especificação: `spec.md`
* Master Plan: `../../Master-plan.md`
* Arquitetura conceitual: `docs/architecture/`
* Decisões: `docs/decisions/`
* Evidências: `docs/diagrams/`

---

## 2. Resumo técnico

Este plano descreve o estado arquitetural observado no repositório, não uma arquitetura alvo futura. A estrutura atual combina camadas conceituais, implementações parciais e infra de dados, e o entendimento correto exige tratá-la como brownfield.

---

## 3. Contexto técnico

### Stack observado

| Tecnologia | Versão / evidência | Uso |
| ---------- | ------------------ | --- |
| React | `view/package.json` | Frontend web. |
| Vite | `view/package.json` | Build e dev server do frontend. |
| Tailwind | `view/package.json` | Estilização do UI. |
| FastAPI | `services/api/analytics/Dockerfile` | API de analytics e endpoints REST. |
| SQLAlchemy | `services/api/analytics/Dockerfile` | Persistência e mapeamento do banco. |
| PostgreSQL | migrações em `database/render/migrations` | Banco de dados principal de apoio operacional e analítico. |
| Airflow | `etl/airflow/docker-compose.airflow.yml` | Orquestração de pipeline ETL. |
| dbt | `etl/dbt/google_trends/dbt_project.yml` | Transformações em `silver` e `gold`. |
| Flyway | `runtime/database/docker-compose.render.yml` | Migração de schemas do banco. |
| Java Spring-like | `services/bff/src/main/java/.../BffApplication.java` | Estrutura do BFF, sem implementação completa. |
| GitHub Actions | `.github/workflows/*.yml` | Automação de migrações de banco e dbt. |

---

## 4. Arquitetura atual

```text
view (React/Vite)
    ↓
BFF (Java, estrutura inicial)
    ├── Serviços operacionais (planejados)
    │   ├── Reservas
    │   └── Pagamentos
    └── Analytics API (FastAPI implementado)
            ↓
      PostgreSQL (schemas segregados)
            ↓
   ETL Airflow + dbt
            ↓
  Silver / Gold analytics views
```

### Observações

- O desenho arquitetural conceitual está documentado em `docs/architecture` e em diagramas Mermaid em `docs/diagrams`.
- O código real existente valida a parte analítica e a infraestrutura data/ETL, mas não documenta conclusivamente a implementação completa de reservas e pagamentos.
- O BFF não foi implementado de forma funcional neste snapshot; seu arquivo principal é apenas um `BffApplication.java` vazio.

---

## 5. Componentes

## C1 — Frontend web

Responsabilidade:

- Interface do usuário para operação e visão de métricas.

Evidência:

- `view/` com `package.json`, `Index.tsx`, `src/` e testes Vitest.

Dependências:

- React, Vite, Tailwind, Radix UI, React Query.

## C2 — API de analytics

Responsabilidade:

- Expor endpoints REST para pacientes, alertas de capacidade e decisões de marketing.

Evidência:

- `services/api/analytics/src/main.py`
- `services/api/analytics/src/interfaces/api/routes.py`
- `services/api/analytics/src/infraestructure/persistence/models.py`

Dependências:

- FastAPI, SQLAlchemy, PostgreSQL.

## C3 — Pipeline ETL de Google Trends

Responsabilidade:

- Extrair dados de tendência de busca, transformar e persistir em staging.

Evidência:

- `etl/airflow/dags/dag_google_trends.py`
- `etl/airflow/dags/services/google_trends/extractor.py`
- `etl/airflow/dags/services/google_trends/mapper.py`

Dependências:

- Airflow, PyTrends, PostgreSQL.

## C4 — Modelagem analytics com dbt

Responsabilidade:

- Construir visões analíticas a partir de staging e dados operacionais.

Evidência:

- `etl/dbt/google_trends/models/gold/gld__capacity_alert.sql`
- `etl/dbt/google_trends/models/gold/gld__mkt_decision_matrix.sql`

Dependências:

- dbt-postgres, schemas `clinic`, `marketing`, `operations`, `staging`, `silver`, `gold`.

## C5 — Banco de dados operacional/analítico

Responsabilidade:

- Guardar dados de clínica, operações, marketing e controle de ETL.

Evidência:

- `database/render/migrations/V20260503__create_clinic.sql`
- `database/render/migrations/V20260504__create_marketing.sql`
- `database/render/migrations/V20260504_1__create_operations.sql`
- `database/render/migrations/V20260502__create_etl_load.sql`

## C6 — BFF

Responsabilidade:

- Agregar dados e adaptar APIs para o frontend.

Status observado:

- Documentado como decisão arquitetural (`docs/decisions/adr-002-bff-pattern.md`), mas sem implementação funcional observável.

## C7 — Reservas e pagamentos

Responsabilidade:

- Fluxos de agendamento e pagamento, com integração externa e eventos de domínio.

Status observado:

- Documentação arquitetural detalha o padrão, mas as implementações concretas não aparecem como componentes completos no snapshot analisado.

---

## 6. Modelo de dados

Os dados observados indicam múltiplos domínios no mesmo banco PostgreSQL, separados por schemata:

```text
clinic
  ├── specialties
  ├── professionals
  ├── professional_schedules
  ├── schedule_exceptions
  ├── patients
  ├── cid_codes
  ├── services
  └── appointments

operations
  └── professional_contracts

marketing
  ├── marketing_search_terms
  └── marketing_benchmarks

staging
  └── stg_google_trends

silver
  └── visões derivadas da transformação

gold
  ├── gld__capacity_alert
  └── gld__mkt_decision_matrix

control
  └── etl_load
```

### Evidência

- `database/render/migrations/V20260503__create_clinic.sql`
- `database/render/migrations/V20260504__create_marketing.sql`
- `database/render/migrations/V20260504_1__create_operations.sql`
- `database/render/migrations/V20260501__create_google_trends.sql`
- `database/render/migrations/V20260502__create_etl_load.sql`

---

## 7. Contratos e fluxos

### Fluxo de analytics

O fluxo observado é:

1. Airflow extrai Google Trends.
2. Salva em `staging.stg_google_trends`.
3. dbt transforma para visões em `silver`/`gold`.
4. FastAPI consulta as visões via SQLAlchemy.
5. API responde métricas e decisões analíticas.

### Fluxo de operação conceitual

A documentação em `docs/diagrams/` descreve:

- criação de reserva;
- emissão de evento de domínio;
- processamento de pagamento;
- atualização do status de reserva;
- integração com gateway externo.

Porém, na implementação observada, esses fluxos não estão plenamente materializados.

---

## 8. Decisões técnicas observadas

## ADR-001 — Separação de agendamento e pagamentos em APIs distintas

### Contexto

Documentado em `docs/decisions/adr-001-separate-booking-and-payments-apis.md`.

### Decisão

Separar agendamento e pagamentos em domínios distintos, com bancos e deploy independentes.

### Consequência observada

A intenção arquitetural é clara, mas a implementação concreta ainda não foi verificada no snapshot analisado.

## ADR-002 — BFF

### Contexto

Documentado em `docs/decisions/adr-002-bff-pattern.md`.

### Decisão

Centralizar orquestração e agregação do frontend em um BFF.

### Consequência observada

Existe documentação e intenção, mas há pouca implementação funcional do BFF neste repositório.

## ADR-003 — Event bus

### Contexto

Documentado em `docs/decisions/adr-003-event-bus-pattern.md`.

### Decisão

Uso de event bus para acoplamento assíncrono entre domínios.

### Consequência observada

Não há sinal consistente de implementação de broker no código neste snapshot.

## ADR-004 — Analytics em banco OLAP

### Contexto

Documentado em `docs/decisions/adr-004-analytics-db.md`.

### Decisão

Separar workloads analíticas em base dedicada.

### Consequência observada

A estrutura do banco com schemas e modelos dbt confirma essa intenção, mas ainda não define um banco analítico separado em deploy explícito.

---

## 9. Estratégia de runtime e deployment

### Infra observada

- `runtime/database/docker-compose.render.yml` define um stack Flyway para migrar o banco em Render.
- `etl/airflow/docker-compose.airflow.yml` define Airflow + PostgreSQL local para orquestração.
- `services/api/analytics/Dockerfile` empacota a API FastAPI em container.
- `runtime/api/analytics/Dockerfile` também empacota a mesma API para runtime específico.

### Evidência de deploy

- `.github/workflows/database-render.yml` executa migrações no Render quando há mudança em `database/render/migrations/**`.
- `.github/workflows/dbt-render.yml` existe, mas o job está desabilitado (`if: false`).

### Limitação

Não há evidência suficiente para afirmar um ambiente de produção completo, load balancer, broker, orquestrador ou pipeline end-to-end totalmente funcional.

---

## 10. Estratégia de testes

| Tipo | Escopo | Evidência |
| ---- | ------ | --------- |
| Frontend unitário | `view` | `package.json` com `vitest run`. |
| Lint | `view` | `eslint .`. |
| CI para banco | Render | `.github/workflows/database-render.yml`. |
| CI dbt | desabilitado | `.github/workflows/dbt-render.yml` com `if: false`. |
| Backend Python | não confirmado | Não há evidência de testes automatizados em `services/api/analytics`. |
| Backend Java | não confirmado | `services/bff` sem testes observáveis no snapshot. |

---

## 11. Observabilidade

A observabilidade é parcialmente definida em documentação, mas faltam implementações evidentes em código. O projeto documenta requisitos de logs estruturados, correlation-id, métricas e latência, mas não há dashboard ou stack observável nesta snapshot.

---

## 12. Segurança

A constituição do projeto exige que secrets e credenciais não sejam armazenados no repositório. A evidência observada não mostra segredos hardcoded. A documentação também evita exposição direta de informações sensíveis.

---

## 13. Rollback

Não há evidência de estratégia formal de rollback implementada no snapshot. A única automação observada é migração de banco via Flyway e ações GitHub para Render.

---

## 14. Riscos

| Risco | Probabilidade | Impacto | Mitigação observada |
| ----- | ------------- | ------- | ------------------ |
| Arquitetura idealizada não corresponde à implementação real | Alta | Alta | Documentação explícita do estado atual e distinção de fatos/inferências |
| BFF não implementado | Alta | Média | Evidência limitada em código; ainda em estrutura inicial |
| Event bus não materializado | Média | Média | Necessidade de confirmação em infra real |
| Ambiguidade de produção | Média | Alta | Documentação não afirma ambiente de produção final |

---

## 15. Constitution Check

| Princípio | Conforme? | Evidência |
| --------- | --------- | --------- |
| Segurança por default | ✅ | Nenhum segredo observado em documentação ou código relevante. |
| Least privilege | ✅ | Não foi identificado uso excessivo de permissões na documentação estudada. |
| Dados sensíveis | ✅ | Esquemas e documentação não expõem dados reais. |
| Reprodutibilidade sem exposição | ✅ | Infra/DB depende de variáveis de ambiente e não de segredos hardcoded. |
| Evidência | ✅ | As afirmações foram cruzadas com arquivos observados. |
| Contexto mínimo | ✅ | O documento foi limitado ao necessário para a arquitetura atual. |

---

## 16. Gaps

* [ ] Nenhuma implementação funcional completa de BFF foi observada.
* [ ] Nenhuma integração completa de pagamentos foi confirmada na base de código.
* [ ] Nenhuma implementação de event bus foi confirmada no runtime atual.
* [ ] Não há documentação formal de deployment de produção para o conjunto completo.
* [ ] O projeto contém arquitetura planejada e implementada em etapas diferentes sem um estado final único.

---

## 17. Decisão de implementação

```text
CURRENT_STATE_DOCUMENTED
```

O objetivo deste plano foi consolidar o entendimento do estado atual do repositório e não iniciar implementação ou tarefas de desenvolvimento.
