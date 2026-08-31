# Especificação: DAG de População de Operations (P3)

## 1. Objetivo

Criar um pipeline (DAG) no Apache Airflow que popule as tabelas do schema `operations` (especificamente `operations.professional_contracts`) com dados sintéticos realistas e coerentes com a realidade operacional da clínica, viabilizando análises de ponto de equilíbrio (*break-even*), alertas de capacidade e cálculo de margem operacional pelo dbt e API de Analytics.

---

## 2. Contexto

A plataforma Marca Platform necessita de dados operacionais e contratuais vinculados aos profissionais de saúde cadastrados no schema `clinic` para:
- Alimentar o modelo analítico `gld__capacity_alert.sql` (visão de ociosidade crítica vs. meta atingida).
- Calcular custos fixos semanais, margem de contribuição por procedimento e volume mínimo de atendimentos (*break-even*).
- Viabilizar testes de capacidade e relatórios gerenciais na camada analítica.

Atualmente, o schema `operations` possui a tabela `operations.professional_contracts`, porém sem dados e sem restrição de unicidade para re-execuções idempotentes.

---

## 3. Requisitos Funcionais

### RF1: População de Contratos Profissionais (`operations.professional_contracts`)
- Vincular contratos a profissionais existentes (`clinic.professionals.professional_id`).
- Associar a especialidade correta do profissional (`clinic.specialties.name`).
- Gerar carga horária semanal contratada realista (entre 20h e 44h semanais).
- Gerar custo fixo semanal compatível com a especialidade e carga horária (R$ 2.000,00 a R$ 6.000,00).
- Atribuir preço base de serviço médio coerente com a especialidade (R$ 150,00 a R$ 500,00).
- Definir custo variável unitário por procedimento (materiais, insumos e comissões: R$ 20,00 a R$ 80,00, garantindo margem de contribuição positiva).
- Calcular e persistir o ponto de equilíbrio (*break-even threshold units*):
  $$\text{be\_threshold\_units} = \left\lceil \frac{\text{weekly\_fixed\_cost}}{\text{service\_price} - \text{variable\_cost\_per\_service}} \right\rceil$$

---

## 4. Requisitos Não-Funcionais

### RNF1: Parametrização e Uso do Utilitário de Mock
- Utilizar `MockDataFactory` (`etl/airflow/dags/utils/mock_data_generator.py`) sem hardcoding.
- Parametrizar quantidades e faixas de valores via configuração.

### RNF2: Idempotência e Upsert
- Adicionar índice/constraint de unicidade em `(professional_id)` via migração Flyway.
- Implementar query com `ON CONFLICT (professional_id) DO UPDATE SET ...` para suportar re-execuções sem duplicatas ou falhas.

### RNF3: Coerência com Domínio Clinic
- Buscar os profissionais e especialidades reais previamente persistidos em `clinic.professionals` e `clinic.specialties` para manter integridade de negócio.

### RNF4: Rastreabilidade com Control Dataset
- Registrar início, sucesso e falha no `control.etl_load` via `ControlRepository`.

### RNF5: Padrão DDD e Camadas
- Seguir a arquitetura: `DAG` $\rightarrow$ `Model (DTO)` $\rightarrow$ `Repository` $\rightarrow$ `PostgresHandler` $\rightarrow$ `PostgreSQL`.

---

## 5. Casos de Teste e Aceitação

### Caso 1: Execução com Profissionais Existentes
- **Entrada**: Profissionais cadastrados no schema `clinic`.
- **Resultado**: Contratos gerados para 100% dos profissionais com `be_threshold_units` calculado corretamente e margem positiva.

### Caso 2: Re-execução Idempotente
- **Entrada**: Re-execução da DAG sobre base já populada.
- **Resultado**: Dados atualizados via `ON CONFLICT` sem duplicação de linhas.

### Caso 3: Execução com Base Vazia
- **Entrada**: Schema `clinic` sem profissionais.
- **Resultado**: DAG finaliza gracefully com 0 registros processados sem estourar exceção não tratada.

---

## 6. Critérios de Aceitação

- [ ] Migração Flyway criada adicionando índice único em `operations.professional_contracts (professional_id)`.
- [ ] DTO `ProfessionalContractModel` criado em `models/operations.py`.
- [ ] Repositório `OperationsRepository` implementado em `infraestructure/repository/operations/`.
- [ ] Query `upsert_professional_contracts.sql` criada com named parameters `:param`.
- [ ] DAG `pipeline_upsert_operations_data` implementada em `dag_upsert_operations.py`.
- [ ] Testes unitários cobrindo DTO, repositório, cálculo de break-even e importação da DAG.
- [ ] Documentação de governança (`spec.md`, `plan.md`, `tasks.md`, `checkpoint.md`) mantida em pt-BR.
