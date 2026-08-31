# Tasks: DAG de População de Operations (P3)

## Tarefas de Implementação

### Fase 1: Infraestrutura de Dados e Modelo DTO
- [x] T001 [RF1] Criar migração Flyway com índice único para `operations.professional_contracts` — `database/render/migrations/V20260506__add_operations_unique_constraints.sql`
- [x] T002 [RF1] Criar query SQL de upsert de contratos com named parameters `:param` — `etl/airflow/dags/infraestructure/repository/operations/queries/upsert_professional_contracts.sql`
- [x] T003 [RF1] Criar modelo Pydantic `ProfessionalContractModel` — `etl/airflow/dags/models/operations.py`

### Fase 2: Repositório de Acesso a Dados
- [x] T004 [RF1] Implementar repositório `OperationsRepository` com métodos de upsert e consulta de profissionais de clinic — `etl/airflow/dags/infraestructure/repository/operations/operations_repo.py`

### Fase 3: Pipeline e Orquestração Airflow
- [x] T005 [RF1, RNF1-5] Implementar a DAG `dag_upsert_operations.py` com tarefas decoradas (`@dag`, `@task`), geração de mocks via `MockDataFactory`, cálculo de break-even e rastreamento via `ControlRepository` — `etl/airflow/dags/dag_upsert_operations.py`

### Fase 4: Validação e Testes
- [x] T006 [RNF1-5] Criar testes unitários para DTO, repositório, cálculo de break-even e importação da DAG — `etl/airflow/dags/tests/test_operations_pipeline.py`
- [x] T007 [RF1] Executar suíte de validação e registrar evidências — `etl/airflow/dags/tests/`

### Fase 5: Checkpoint e Finalização
- [x] T008 [GOV] Atualizar `docs/issues/dag-de-populacao-de-operations/checkpoint.md` e `docs/issues/Master-plan.md` — `docs/issues/dag-de-populacao-de-operations/checkpoint.md`
