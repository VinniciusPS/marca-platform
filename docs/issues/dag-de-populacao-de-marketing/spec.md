# Especificação: DAG de População de Marketing (P4)

## 1. Objetivo

Criar um pipeline (DAG) no Apache Airflow que popule as tabelas do schema `marketing` (`marketing.marketing_search_terms` e `marketing.marketing_benchmarks`) com dados sintéticos realistas e coerentes com as especialidades médicas cadastradas na clínica, viabilizando análises de CAC projetado, elasticidade de demanda e simulações na matriz de decisão de marketing (`gld__mkt_decision_matrix.sql`).

---

## 2. Contexto

O sistema Marca Platform utiliza dados de marketing para cruzar o interesse de busca (Google Trends) com métricas de investimento e aquisição por especialidade:
- `marketing.marketing_search_terms`: Armazena termos de busca associados a cada especialidade médica para orientar extrações de tendências e campanhas.
- `marketing.marketing_benchmarks`: Define parâmetros econômicos de mídia de performance (CPC base, CVR base, elasticidade e teto de margem líquida pós-CAC).

Essas tabelas alimentam o modelo dbt `gld__mkt_decision_matrix.sql`, que classifica as especialidades em estratégias como "Agressividade Permitida", "Limite de Operação" ou "Bid Baixo".

---

## 3. Requisitos Funcionais

### RF1: População de Termos de Busca (`marketing.marketing_search_terms`)
- Associar termos de busca realistas e contextualizados para cada especialidade cadastrada (`clinic.specialties.specialty_id`).
- Gerar termos relevantes em português (ex.: "dentista", "aparelho ortodôntico", "cardiologista", "exame de ecocardiograma", etc.).
- Garantir unicidade da combinação `(specialty_id, search_term)`.

### RF2: População de Benchmarks de Marketing (`marketing.marketing_benchmarks`)
- Criar benchmarks para cada especialidade (`specialty`).
- Gerar custo por clique base realista (`base_cpc` entre R$ 1,50 e R$ 7,50).
- Gerar taxa de conversão base realista (`base_cvr` entre 2,0% e 8,5%, ex.: 0.0200 a 0.0850).
- Gerar índice de elasticidade de preço/demanda (`elasticity_score` entre 0.50 e 1.30).
- Gerar teto de margem líquida para absorção de CAC (`net_margin_limit` entre R$ 120,00 e R$ 450,00).
- Garantir unicidade em `(specialty)` para suportar atualizações idempotentes.

---

## 4. Requisitos Não-Funcionais

### RNF1: Parametrização e Uso do Utilitário de Mock
- Utilizar `MockDataFactory` (`etl/airflow/dags/utils/mock_data_generator.py`) sem hardcoding.
- Configurar schemas e faixas de valores via `generate()`.

### RNF2: Idempotência e Upsert
- Criar migração Flyway adicionando índices de unicidade compostos para suportar cláusulas `ON CONFLICT`.
- Implementar queries SQL de *upsert* com named parameters `:param`.

### RNF3: Coerência com Domínio Clinic
- Consultar especialidades reais de `clinic.specialties` para manter integridade relacional.

### RNF4: Rastreabilidade com Control Dataset
- Registrar início, sucesso e falha no `control.etl_load` via `ControlRepository`.

### RNF5: Padrão DDD e Camadas
- Seguir a arquitetura: `DAG` $\rightarrow$ `Model (DTO)` $\rightarrow$ `Repository` $\rightarrow$ `PostgresHandler` $\rightarrow$ `PostgreSQL`.

---

## 5. Critérios de Aceitação

- [ ] Migração Flyway criada com índices únicos para `marketing.marketing_search_terms` e `marketing.marketing_benchmarks`.
- [ ] DTOs `MarketingSearchTermModel` e `MarketingBenchmarkModel` criados em `models/marketing.py`.
- [ ] Repositório `MarketingRepository` implementado em `infraestructure/repository/marketing/`.
- [ ] Queries SQL de upsert e consulta criadas em `infraestructure/repository/marketing/queries/`.
- [ ] DAG `pipeline_upsert_marketing_data` implementada em `dag_upsert_marketing.py`.
- [ ] Testes unitários cobrindo DTOs, repositório e DAG passando com 100% de sucesso.
