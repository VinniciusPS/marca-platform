# Checkpoint: DAG de População de Marketing (P4)

## 1. Estado Atual
- **Status**: IN_PROGRESS
- **Fase Atual**: Fase 1 (Infraestrutura e Modelos DTO)
- **Data/Hora**: 2026-08-31

---

## 2. Tarefas Concluídas
- [x] Especificação formalizada (`docs/issues/dag-de-populacao-de-marketing/spec.md`)
- [x] Plano de implementação aprovado (`docs/issues/dag-de-populacao-de-marketing/plan.md`)
- [x] Lista de tarefas executáveis criada (`docs/issues/dag-de-populacao-de-marketing/tasks.md`)

---

## 3. Tarefas Pendentes
- [ ] T001: Migração Flyway com índices de unicidade.
- [ ] T002: Queries SQL isoladas.
- [ ] T003: Modelos DTO em `models/marketing.py`.
- [ ] T004: `MarketingRepository`.
- [ ] T005: DAG `dag_upsert_marketing.py`.
- [ ] T006 - T007: Testes unitários e validação.
- [ ] T008: Checkpoint final e atualização do Master Plan.

---

## 4. Decisões Tomadas
- Inclusão de índices únicos em `marketing_search_terms (specialty_id, search_term)` e `marketing_benchmarks (specialty)`.
- Uso do `MockDataFactory` agnóstico para gerar termos de busca e faixas de CPC/CVR/elasticidade.
- Queries SQL 100% isoladas no subdiretório `queries/` com named parameters `:param`.
