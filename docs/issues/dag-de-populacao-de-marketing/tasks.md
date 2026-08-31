# Tasks: DAG de População de Marketing (P4)

## Tarefas de Implementação

### Fase 1: Infraestrutura de Dados e Modelos DTO
- [ ] T001 [RF1, RF2] Criar migração Flyway com índices únicos para o schema marketing — `database/render/migrations/V20260507__add_marketing_unique_constraints.sql`
- [ ] T002 [RF1, RF2] Criar queries SQL de upsert e consulta em arquivos isolados — `etl/airflow/dags/infraestructure/repository/marketing/queries/`
- [ ] T003 [RF1, RF2] Criar modelos Pydantic `MarketingSearchTermModel` e `MarketingBenchmarkModel` — `etl/airflow/dags/models/marketing.py`

### Fase 2: Repositório de Acesso a Dados
- [ ] T004 [RF1, RF2] Implementar repositório `MarketingRepository` — `etl/airflow/dags/infraestructure/repository/marketing/marketing_repo.py`

### Fase 3: Pipeline e Orquestração Airflow
- [ ] T005 [RF1, RF2, RNF1-5] Implementar a DAG `dag_upsert_marketing.py` com tarefas decoradas (`@dag`, `@task`), geração parametrizada via `MockDataFactory` e rastreamento via `ControlRepository` — `etl/airflow/dags/dag_upsert_marketing.py`

### Fase 4: Validação e Testes
- [ ] T006 [RNF1-5] Criar testes unitários para DTOs, repositório e DAG — `etl/airflow/dags/tests/test_marketing_pipeline.py`
- [ ] T007 [RF1, RF2] Executar suíte de validação e registrar evidências — `etl/airflow/dags/tests/`

### Fase 5: Checkpoint e Finalização
- [ ] T008 [GOV] Atualizar `docs/issues/dag-de-populacao-de-marketing/checkpoint.md` e `docs/issues/Master-plan.md` — `docs/issues/dag-de-populacao-de-marketing/checkpoint.md`
