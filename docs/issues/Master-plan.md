# Master Plan

> Documento de governança do estado atual do repositório. Este arquivo consolida a visão global do sistema e serve como referência para a arquitetura existente em brownfield, sem transformar a documentação em backlog de implementação.

## 1. Visão do projeto

O repositório representa uma plataforma de gestão para operações de clínica/serviços, com foco em:

- agendamento de serviços;
- pagamentos vinculados a agendamento;
- analytics operacional e de marketing;
- ETL e modelos analíticos para apoio à decisão.

A estrutura atual mistura:

- documentação de arquitetura conceitual e decisões;
- implementações parciais em Python e Java;
- infraestrutura de banco e ETL em Postgres + Airflow + dbt;
- frontend em React/Vite.

## 2. Estado observado

### Fatos observados

- O diretório `view/` contém um frontend React + Vite + Tailwind, com scripts de build/test.
- O diretório `services/bff/` contém um projeto Java com `BffApplication.java`, mas sem implementação funcional relevante.
- O diretório `services/api/analytics/` contém uma API FastAPI funcional, com rotas de pacientes e endpoints de analytics.
- O diretório `services/api/payments/` contém apenas um ponto de entrada FastAPI mínimo.
- O diretório `services/api/booking/` contém apenas um README com estrutura de arquitetura planejada.
- O diretório `etl/airflow/` contém DAGs, repositórios e serviços para extração de `Google Trends` e persistência em PostgreSQL.
- O diretório `etl/dbt/google_trends/` contém modelos `dbt` para montar visões em `silver` e `gold`.
- O diretório `database/render/migrations/` contém migrações Flyway para `clinic`, `marketing`, `operations`, `staging`, `silver`, `gold` e `control`.
- O diretório `.github/workflows/` ativa migração de banco Render e uma workflow de dbt com trigger desabilitado.
- A documentação arquitetural em `docs/architecture/` e `docs/decisions/` descreve um modelo de domínios separados com BFF, event bus e analytics em banco OLAP.

### Inferências válidas

- O projeto usa uma abordagem de múltiplos serviços e domínios, mas ainda existe uma discrepância entre arquitetura desejada e implementação atual.
- O componente de analytics possui maior grau de concretude do que reserva, pagamento e BFF.
- O banco de dados e o pipeline ETL parecem ser a base das decisões de analytics e marketing.

### Hipóteses

- O repositório está em transição de arquitetura conceitual para implementação por partes.
- Os serviços de reservas e pagamentos ainda não foram finalizados ou não estão embarcados neste snapshot.

### Incógnitas

- Não foi possível confirmar a infraestrutura de produção real, credenciais, URLs e ambiente final.
- Não foi possível confirmar o uso de broker/event bus em produção, pois o código não expõe uma implementação completa.
- Não foi possível confirmar se o BFF e a API de pagamentos serão entregues por um stack diferente da API de analytics.

## 3. Prioridade de problemas

| Ordem | ID | Problema | Status | Dependências |
| ----: | -- | -------- | ------ | ------------ |
| 1 | P1 | Estado atual da arquitetura | COMPLETED | — |
| 2 | P2 | DAG de população de clinic | COMPLETED | P1 |

## 4. Mapa estrutural do sistema

| Camada | Local | Observação |
| --- | --- | --- |
| Frontend | `view/` | Aplicação web em React/Vite com UI e testes via Vitest. |
| BFF | `services/bff/` | Estrutura inicial em Java; implementação funcional incompleta. |
| API Analytics | `services/api/analytics/` | FastAPI com rotas de paciente e analytics, acessando Postgres via SQLAlchemy. |
| API Pagamentos | `services/api/payments/` | Ponto de entrada mínimo; sem fluxo completo identificado. |
| API Reservas | `services/api/booking/` | Apenas estrutura de referência/planejada; sem implementação funcional. |
| ETL | `etl/airflow/` | Extração e persistência de Google Trends em Postgres. |
| Transformação | `etl/dbt/google_trends/` | Modelagem em `silver`/`gold` para alertas de capacidade e decisão de marketing. |
| Dados | `database/render/migrations/` | Schemas e tabelas de operações, clínica, marketing e controle. |
| Deploy | `runtime/`, `deploy/`, `.github/workflows/` | Infra de banco e automação de migração; pouca evidência de runtime completo. |

## 4. Observações de arquitetura

### 4.1 Componentes e domínios

O sistema foi modelado como:

- frontend web;
- BFF de composição;
- serviços de domínio separados para reservas e pagamentos;
- API de analytics;
- camada analítica alimentada por ETL.

A documentação em `docs/decisions` indica que a intenção arquitetural é clara: minimalização de acoplamento entre domínios, analytics isolado e BFF como orquestrador da UI.

### 4.2 Persistência

O banco de dados é PostgreSQL, com schemas separados:

- `clinic` — pacientes, profissionais, agendas, agendamentos, serviços e especialidades;
- `operations` — contratos profissionais;
- `marketing` — termos e benchmarks de marketing;
- `staging` — dados brutos de carga ETL;
- `silver` — modelos enriquecidos/transformados;
- `gold` — visões analíticas consumidas pela API;
- `control` — histórico de cargas ETL.

### 4.3 Fluxos de dados

- O Airflow extrai dados de Google Trends e grava em `staging.stg_google_trends`.
- Os modelos dbt transformam os dados em visões de `gold`.
- A API de analytics lê as visões em `silver`/`gold` através do SQLAlchemy e expõe endpoints REST.
- A base de dados operacional e a base analítica não são separadas em arquivo de deploy explícito; a evidência aponta para um único PostgreSQL compartilhado com schemas segregados.

### 4.4 Integrações externas

- `Google Trends` via `pytrends` no Airflow.
- `Pagamento externo` sinalizado em documentação e diagramas, mas sem implementação concreta neste snapshot.

### 4.5 Testes e CI/CD

- Frontend: `vitest run` e lint com ESLint.
- Workflow GitHub Actions: migração Flyway para Render.
- Workflow dbt está desabilitada por `if: false`.
- Não há evidência de suíte automatizada para serviços backend Python/Java neste snapshot.

## 5. Riscos de entendimento do estado atual

- O código não representa um sistema totalmente integrado em produção.
- Há divergência entre documentação arquitetural idealizada e implementação concreta.
- O repositório contém artefatos em diferentes níveis de maturidade (conceitual, planejado, parcial e funcional).

## 6. Conclusão

O repositório descreve um sistema de plataforma em evolução com arquitetura explicitamente orientada a domínios, BFF, analytics e ETL. A evidência mostra um estado brownfield: a arquitetura desejada está documentada e parcialmente traduzida em infraestrutura e código, mas ainda faltam integrações e serviços completos para atingir a visão apresentada em `docs/diagrams` e `docs/decisions`.

## 7. Registro de estado

```text
Status: CURRENT_STATE_DOCUMENTED
Tipo: arquitetura existente / brownfield
Escopo documental: concluído
Tasks de implementação: não criadas conforme solicitação do usuário
```
