# Especificação: DAG de População de Clinic (P2)

## 1. Objetivo

Criar um pipeline (DAG) que popule as tabelas do schema `clinic` com dados realistas via mock, preparando o ambiente para testes de analytics e funcionamento de agendamento.

## 2. Contexto

O sistema Marca Platform necessita de dados de teste coerentes para:
- Validar fluxos de agendamento e pagamento
- Treinar modelos de analytics
- Testar lógica de relatórios operacionais
- Demonstrar funcionalidade da plataforma

Atualmente, o schema `clinic` existe mas está vazio. A solução é criar um DAG que popule de forma realista.

## 3. Arquivos a Criar

```
dags/
├── dag_upsert_clinic.py                          # DAG principal (clinic-specific)
├── models/clinic.py                              # DTOs (8 entidades clinic)
├── utils/
│   ├── mock_data_generator.py                    # GENÉRICO: MockDataFactory
│   └── __init__.py
└── infraestructure/repository/clinic/
    ├── clinic_repo.py                            # Repository upsert
    ├── queries/
    │   ├── upsert_specialties.sql
    │   ├── upsert_professionals.sql
    │   ├── upsert_professional_schedules.sql
    │   ├── upsert_schedule_exceptions.sql
    │   ├── upsert_patients.sql
    │   ├── upsert_cid_codes.sql
    │   ├── upsert_services.sql
    │   └── upsert_appointments.sql
    └── __init__.py
```

**Apenas 2 arquivos são genéricos:**
- `dags/utils/mock_data_generator.py` — Reutilizável para qualquer DAG
- Tudo mais é específico do clinic


### RF1: População de Especialidades
- Criar especialidades realistas (e.g., Odontologia, Cardiologia, Dermatologia)
- Quantidade parametrizável
- Garantir unicidade de nomes

### RF2: População de Profissionais
- Criar profissionais associados a especialidades
- Gerar documentos únicos (CRM ou CPF)
- Nomes realistas
- Status ativo por padrão

### RF3: População de Agendas de Profissionais
- Criar disponibilidade semanal realista (seg-sex, 08:00-17:00)
- Respeitar relacionamento com profissionais
- Permitir diferentes horários por profissional

### RF4: População de Exceções de Agenda
- Criar ausências realistas (férias, feriados)
- Data/hora válidas
- Motivos descritivos

### RF5: População de Pacientes
- Criar pacientes com nomes realistas
- CPF único (quando presente)
- Data de criação consistente

### RF6: População de Códigos CID
- Criar códigos CID realistas (saúde)
- Descrições de diagnósticos
- Quantidade parametrizável

### RF7: População de Serviços
- Criar serviços por especialidade
- Preços base realistas
- Nomes descritivos

### RF8: População de Agendamentos
- Criar agendamentos válidos (paciente, profissional, serviço, data)
- Status variado (scheduled, completed, cancelled)
- Respeitar disponibilidade de profissionais
- Preços finais realistas

## 4. Requisitos Não-Funcionais

### RNF1: Parametrização
- Mock aceita argumento `rows_quantity` para controlar volume
- Sem hardcoding de quantidades
- Facilita testes com volumes diferentes

### RNF2: Upsert
- Usar estratégia ON CONFLICT para evitar duplicatas em re-execuções
- Repository implementa upsert, não apenas insert

### RNF3: Performance
- Processar dados em lotes (não carrega tudo na memória)
- Generator para stream de dados

### RNF4: Realismo
- Nomes, documentos e dados contextualizados
- Não usar dados genéricos ("test_1", "value_1")
- Datas coerentes

### RNF5: Sem Serviços Externos
- DAG não usa API externa
- Mock implementado em Python puro
- Sem dependências adicionais

## 5. Arquitetura

```
dag_upsert_clinic.py (DAG específica do clinic)
  ├── @task generate_specialties(): configura e chama MockDataFactory
  ├── @task generate_professionals(): configura e chama MockDataFactory
  ├── @task generate_patients(): configura e chama MockDataFactory
  ├── ... (uma task por entidade)
  ├── models/clinic.py (DTOs de domínio)
  └── infraestructure/repository/clinic/clinic_repo.py (Repository)

dags/utils/mock_data_generator.py (GENÉRICO - Shared)
  └── MockDataFactory: classe agnóstica que gera dados baseado em config
      └── generate(field_definitions, rows_quantity) → Generator[dict]

infraestructure/repository/clinic/queries/ (SQL)
  ├── upsert_specialties.sql
  ├── upsert_professionals.sql
  ├── upsert_professional_schedules.sql
  ├── upsert_schedule_exceptions.sql
  ├── upsert_patients.sql
  ├── upsert_cid_codes.sql
  ├── upsert_services.sql
  └── upsert_appointments.sql
```

**Separação clara:**
- `dag_upsert_clinic.py`: Orquestração + configuração específica do clinic
- `dags/utils/mock_data_generator.py`: Lógica pura de geração (reutilizável)
- `infraestructure/repository/clinic/`: Persistência (reutiliza pattern existente)



## 6. Fluxo de Dados (Detalhado)

```
@task generate_specialties(rows_quantity=N):
  config = {
    "name": {"type": "str", "realistic": True},
    ...
  }
  for record in MockDataFactory.generate(config, rows_quantity):
    yield SpecialtyDTO(**record)
        ↓
@task load_specialties(raw_data: list):
  SpecialtyRepository.upsert_batch(raw_data)
        ↓
Database (clinic.specialties)

Repete para: professionals, professional_schedules, 
schedule_exceptions, patients, cid_codes, services, appointments
```

**Benefício do MockDataFactory genérico:**
```
# Clinic
MockDataFactory.generate(clinic_config, 100)

# Operations (futuro)
MockDataFactory.generate(operations_config, 100)

# Marketing (futuro)
MockDataFactory.generate(marketing_config, 100)

Mesma classe, configurações diferentes.
```


## 7. Casos de Teste

### Caso 1: Execução inicial vazia
- Entrada: rows_quantity=10
- Resultado: 10 especialidades, 20 profissionais, 100+ agendamentos
- Validação: dados coerentes e únicos

### Caso 2: Re-execução (idempotência)
- Entrada: mesmos parâmetros
- Resultado: sem duplicatas, upsert funciona
- Validação: linhas afetadas = 0 (ou atualiza se necessário)

### Caso 3: Volume grande
- Entrada: rows_quantity=1000
- Resultado: processo completa em < 30s
- Validação: memória controlada (streaming)

## 8. Dependências

- `pydantic` — DTOs (já existe)
- Gerador de dados realistas (sem `faker`, usar listas locais)
- `sqlalchemy` — ORM (já existe)
- `psycopg2` — Driver PostgreSQL (já existe)

## 9. Critérios de Aceitação

- [ ] DAG criada e registrada em Airflow
- [ ] Mock gera dados realistas e parametrizáveis
- [ ] Repository implementa upsert para todas as tabelas
- [ ] Pipeline popula 100% das tabelas clinic
- [ ] Dados são coerentes (FK, tipos, ranges)
- [ ] Re-execução não cria duplicatas
- [ ] Documentação clara de uso

## 10. Métricas de Sucesso

- Pipeline executa sem erros
- Todas as tabelas clinic possuem dados
- Dados passam em validação básica (constraints do BD)
- Tempo de execução < 60s com rows_quantity=100
- Mock reutilizável para outros testes

---

**Status**: SPEC_READY_FOR_REVIEW  
**Data**: 2026-08-30  
**Próximo**: Validação da especificação → Plano → Implementação
