# Tasks: DAG de População de Clinic (P2)

## Tarefas de Implementação

### Fase 1: Infraestrutura de Dados e Ajuste de Queries
- [x] T001 [RF1-8] Criar migração Flyway com índices/constraints de unicidade para o schema clinic — `database/render/migrations/V20260505__add_clinic_unique_constraints.sql`
- [x] T002 [RNF2] Adicionar método `fetch_all` em `PostgresHandler` para consulta de chaves relacionais — `etl/airflow/dags/infraestructure/database/postgres/postgres_handler.py`
- [x] T003 [RF1] Atualizar query de upsert de especialidades para sintaxe `:param` — `etl/airflow/dags/infraestructure/repository/clinic/queries/upsert_specialties.sql`
- [x] T004 [RF2] Atualizar query de upsert de profissionais para sintaxe `:param` — `etl/airflow/dags/infraestructure/repository/clinic/queries/upsert_professionals.sql`
- [x] T005 [RF3] Atualizar query de upsert de disponibilidades de agenda para sintaxe `:param` — `etl/airflow/dags/infraestructure/repository/clinic/queries/upsert_professional_schedules.sql`
- [x] T006 [RF4] Atualizar query de upsert de exceções de agenda para sintaxe `:param` — `etl/airflow/dags/infraestructure/repository/clinic/queries/upsert_schedule_exceptions.sql`
- [x] T007 [RF5] Atualizar query de upsert de pacientes para sintaxe `:param` — `etl/airflow/dags/infraestructure/repository/clinic/queries/upsert_patients.sql`
- [x] T008 [RF6] Atualizar query de upsert de códigos CID para sintaxe `:param` — `etl/airflow/dags/infraestructure/repository/clinic/queries/upsert_cid_codes.sql`
- [x] T009 [RF7] Atualizar query de upsert de serviços para sintaxe `:param` — `etl/airflow/dags/infraestructure/repository/clinic/queries/upsert_services.sql`
- [x] T010 [RF8] Atualizar query de upsert de agendamentos para sintaxe `:param` — `etl/airflow/dags/infraestructure/repository/clinic/queries/upsert_appointments.sql`

### Fase 2: Repositório de Acesso a Dados
- [x] T011 [RF1-8] Implementar `ClinicRepository` com métodos de carga em lote (`upsert_*`) e recuperação de IDs relacionais (`get_*`) — `etl/airflow/dags/infraestructure/repository/clinic/clinic_repo.py`

### Fase 3: Pipeline e Orquestração Airflow
- [x] T012 [RF1-8, RNF1-5] Implementar a DAG `dag_upsert_clinic.py` com tarefas atômicas decoradas (`@dag`, `@task`), geração via `MockDataFactory`, dependências topológicas e rastreamento via `ControlRepository` — `etl/airflow/dags/dag_upsert_clinic.py`

### Fase 4: Validação e Testes
- [x] T013 [RNF1-5] Criar testes unitários e de integração validando DTOs, geração de mocks, queries e execução de pipeline — `etl/airflow/dags/tests/test_clinic_pipeline.py`
- [x] T014 [RF1-8] Executar suíte de validação e registrar evidências — `etl/airflow/dags/tests/`

### Fase 5: Checkpoint e Finalização
- [x] T015 [GOV] Atualizar `docs/issues/dag-de-populacao-de-clinic/checkpoint.md` com status de conclusão e validações — `docs/issues/dag-de-populacao-de-clinic/checkpoint.md`
