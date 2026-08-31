# Padrão de Desenvolvimento de DAGs

Guia de desenvolvimento para DAGs no Airflow da Marca Platform, baseado em Arquitectura em Camadas e Domain-Driven Design (DDD).

## Visão Geral

As DAGs deste projeto seguem uma arquitetura em camadas que separa responsabilidades de forma clara e testável:

```
DAG (Orquestração)
  ↓
Services (Lógica de Negócio)
  ├── Extrator
  ├── Mapper
  └── Validador
  ↓
Infrastructure (Acesso a Recursos)
  ├── Repository (Padrão de Acesso a Dados)
  ├── Database Handlers
  └── External Gateway
  ↓
Models (Contrato e Domínio)
  ├── DTO (Data Transfer Objects)
  ├── Entities
  └── Value Objects
```

## Princípios Fundamentais

### 1. Separação de Responsabilidades
- **Extração** é responsabilidade exclusiva do `Extractor`
- **Transformação** é responsabilidade exclusiva do `Mapper`
- **Persistência** é responsabilidade exclusiva do `Repository`
- **Orquestração** é responsabilidade exclusiva da `DAG`

Cada componente foca em UMA responsabilidade e a faz bem.

### 2. Contrato de Dados (DTOs)
Cada camada conversa através de Data Transfer Objects:

```
Fonte Externa → RawDTO → Mapper → StorageDTO → Database
```

DTOs definem o contrato implícito entre componentes:
- RawDTO: contrato entre Extrator e Mapper (dados brutos processados)
- StorageDTO: contrato entre Mapper e Repository (dados prontos para persistência)

### 3. Mock Data Generator (Shared Generic Utility)

```python
# dags/utils/mock_data_generator.py
from typing import Generator, Dict, Any

class MockDataFactory:
    """
    Gerador agnóstico de dados mock.
    
    Reutilizável para qualquer domínio (clinic, operations, marketing, etc.)
    Configuração define COMO gerar, não O QUÊ gerar.
    """
    
    def generate(self, field_definitions: Dict[str, Dict], rows_quantity: int) -> Generator[Dict[str, Any], None, None]:
        """
        Gera dados baseado em definição de campos.
        
        Exemplo de field_definitions:
        {
            "name": {"type": "str", "pattern": "realistic_name"},
            "cpf": {"type": "str", "pattern": "cpf", "unique": True},
            "created_at": {"type": "datetime", "auto": True}
        }
        """
        for i in range(rows_quantity):
            record = {}
            for field_name, field_config in field_definitions.items():
                record[field_name] = self._generate_value(field_config, i)
            yield record
    
    def _generate_value(self, config: Dict, row_index: int) -> Any:
        """Gera valor único baseado em configuração."""
        field_type = config.get("type")
        pattern = config.get("pattern")
        # TODO: implementar geração por tipo e padrão
        pass
```

**Uso no DAG clinic:**

```python
@task
def generate_specialties(rows_quantity: int = 10):
    config = {
        "name": {"type": "str", "pattern": "specialty_name"},
    }
    factory = MockDataFactory()
    raw_data = []
    for record in factory.generate(config, rows_quantity):
        raw_data.append(SpecialtyDTO(**record).model_dump(mode="json"))
    return raw_data
```

**Nota:** Configuração específica (especialties, profissionais, etc.) fica **dentro da task**, não em arquivo separado.

Sempre que possível, use generators para processar dados em lotes:

```python
# Bom: eficiente em memória
yield from extractor.fetch_stream(...)

# Evitar: carrega tudo na memória
data = list(extractor.fetch_all(...))
```

### 4. Serialização com XCom
O Airflow passa dados entre tasks através de XCom. DTOs Pydantic se serializam automaticamente:

```python
# Extrator retorna lista de dicts (JSON-serializable)
return [raw.model_dump(mode="json") for raw in raw_stream]

# Outra task reconstrói os DTOs
raw_dtos = (RawDTO(**d) for d in raw_data)
```

### 5. Controle de Execução (Control Dataset)
Toda DAG deve registrar seu estado de execução:

```python
# Início
load_id = control_repo.create_initial_load(dataset_name)

# Sucesso
control_repo.update_load_status(ETLLoadDTO(..., status=LoadStatus.SUCCESS))

# Falha
control_repo.update_load_status(ETLLoadDTO(..., status=LoadStatus.FAILED))
```

---

## Estrutura de Diretórios

```
etl/airflow/dags/
├── dag_<dataset_name>.py           # Arquivo principal da DAG
│
├── models/
│   ├── <dataset_name>.py           # DTOs do domínio
│   ├── control.py                  # Modelos de controle (compartilhado)
│   └── __init__.py
│
├── services/
│   └── <dataset_name>/
│       ├── extractor.py            # Gateway para fonte externa
│       ├── mapper.py               # Transformação de dados
│       ├── validator.py            # Validação (opcional)
│       └── __init__.py
│
└── infraestructure/
    ├── database/
    │   ├── postgres/
    │   │   ├── connection.py       # Criação de engine
    │   │   ├── postgres_handler.py # Execução de queries
    │   │   └── __init__.py
    │   └── base_handler.py
    │
    ├── repository/
    │   ├── <dataset_name>/
    │   │   ├── <dataset_name>_repo.py
    │   │   ├── queries/
    │   │   │   ├── upsert.sql
    │   │   │   ├── insert.sql
    │   │   │   └── update.sql
    │   │   └── __init__.py
    │   │
    │   ├── control/
    │   │   ├── control_repo.py
    │   │   └── __init__.py
    │   │
    │   └── __init__.py
    │
    └── __init__.py
```

---

## Componentes Padrão

### 1. Model (DTO)

```python
# models/dataset_name.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class <Dataset>RawDTO(BaseModel):
    """
    Contrato entre Extrator e Mapper.
    Reflete os dados brutos já processados pela fonte.
    """
    field1: str
    field2: int
    extracted_at: datetime

class <Dataset>StorageDTO(BaseModel):
    """
    Contrato entre Mapper e Repository.
    Reflete exatamente o que será persistido.
    """
    model_config = ConfigDict(from_attributes=True)
    
    field1: str
    field2: int
    transformed_at: datetime
    created_at: datetime
```

**Boas Práticas:**
- Use type hints explícitos
- Documente a responsabilidade de cada DTO
- RawDTO reflete a fonte (campo por campo)
- StorageDTO reflete o schema (com timestamps)

### 2. Extrator (Service)

```python
# services/dataset_name/extractor.py
from typing import Generator
from models.dataset_name import <Dataset>RawDTO

class <Dataset>Extractor:
    """
    Gateway para a fonte externa.
    Responsabilidade: Traduzir dados brutos para RawDTO.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("API_KEY")
    
    def fetch_stream(self, params: dict) -> Generator[<Dataset>RawDTO, None, None]:
        """
        Entrega um stream de objetos do domínio.
        Generator = eficiência de memória para grandes volumes.
        """
        for page in self._paginate(**params):
            for record in page:
                yield self._map_to_dto(record)
    
    def _paginate(self, **params):
        """Iteração sobre recursos paginados."""
        page = 1
        while True:
            response = self._request(page=page, **params)
            if not response.get('data'):
                break
            yield response['data']
            page += 1
    
    def _request(self, **params):
        """Abstração da chamada externa."""
        # TODO: implementar com retry, timeout, etc.
        pass
    
    def _map_to_dto(self, record: dict) -> <Dataset>RawDTO:
        """Conversão de dict → RawDTO."""
        return <Dataset>RawDTO(
            field1=record['source_field1'],
            field2=int(record['source_field2']),
            extracted_at=datetime.now()
        )
```

**Boas Práticas:**
- Uma única responsabilidade: extração
- Implementar retry/timeout/rate-limit internamente
- Retornar sempre um stream (generator), não lista
- Não fazer transformações complexas (é trabalho do Mapper)

### 3. Mapper (Service)

```python
# services/dataset_name/mapper.py
from typing import Generator
from models.dataset_name import <Dataset>RawDTO, <Dataset>StorageDTO

class <Dataset>Mapper:
    """
    Transformação de domínio.
    Responsabilidade: Converter RawDTO → StorageDTO.
    """
    
    def transform_stream(self, raw_dtos: Generator[<Dataset>RawDTO, None, None]) -> Generator[<Dataset>StorageDTO, None, None]:
        """
        Processa stream e entrega novo stream.
        """
        now = datetime.now()
        for raw in raw_dtos:
            yield self._transform(raw, now)
    
    def _transform(self, raw: <Dataset>RawDTO, now: datetime) -> <Dataset>StorageDTO:
        """Lógica de transformação."""
        return <Dataset>StorageDTO(
            field1=raw.field1.upper(),
            field2=raw.field2 * 100,
            transformed_at=now,
            created_at=now
        )
    
    def _enrich(self, raw: <Dataset>RawDTO) -> dict:
        """Enriquecimento de dados (se necessário)."""
        # TODO: lookup em dicts, queries auxiliares, etc.
        pass
```

**Boas Práticas:**
- Uma única responsabilidade: transformação
- Receber stream, retornar stream
- Cálculos, conversões, enriquecimentos aqui
- Não fazer I/O externo (é trabalho do Extrator/Repository)

### 4. Repository (Infrastructure)

```python
# infraestructure/repository/dataset_name/dataset_name_repo.py
import os
from typing import List
from models.dataset_name import <Dataset>StorageDTO
from infraestructure.database.postgres.postgres_handler import PostgresHandler

class <Dataset>Repository:
    """
    Padrão de Acesso a Dados.
    Responsabilidade: Persistência agnóstica de domínio.
    """
    
    def __init__(self, handler: PostgresHandler):
        self.handler = handler
        self._query_path = os.path.join(os.path.dirname(__file__), "queries/upsert.sql")
    
    def _get_query(self, operation: str) -> str:
        """Carrega query SQL do arquivo."""
        query_file = os.path.join(
            os.path.dirname(__file__),
            "queries",
            f"{operation}.sql"
        )
        with open(query_file, "r") as f:
            return f.read()
    
    def upsert_batch(self, entities: List[<Dataset>StorageDTO]) -> int:
        """
        Recebe lista de StorageDTO e persiste com UPSERT.
        """
        if not entities:
            return 0
        
        query = self._get_query("upsert")
        data = [entity.model_dump() for entity in entities]
        
        return self.handler.execute_upsert(query, data)
    
    def insert_batch(self, entities: List[<Dataset>StorageDTO]) -> int:
        """INSERT puro (sem update)."""
        if not entities:
            return 0
        
        query = self._get_query("insert")
        data = [entity.model_dump() for entity in entities]
        
        return self.handler.execute_insert(query, data)
```

**Boas Práticas:**
- Receber apenas objetos de domínio (DTOs)
- Queries em arquivos SQL separados
- Métodos com intenção clara (upsert, insert, update)
- Retornar resultado da operação (linhas afetadas)

---

## DAG Principal

```python
# dag_dataset_name.py
import os
from datetime import datetime
from typing import List

from models.control import ETLLoadDTO, LoadStatus
from models.dataset_name import <Dataset>RawDTO, <Dataset>StorageDTO
from infraestructure.database.postgres.connection import get_engine
from infraestructure.database.postgres.postgres_handler import PostgresHandler
from infraestructure.repository.control.control_repo import ControlRepository
from infraestructure.repository.dataset_name.dataset_name_repo import <Dataset>Repository
from services.dataset_name.extractor import <Dataset>Extractor
from services.dataset_name.mapper import <Dataset>Mapper

from airflow.decorators import dag, task
from airflow.utils.trigger_rule import TriggerRule

@dag(
    dag_id="pipeline_dataset_name",
    start_date=datetime(2024, 1, 1),
    schedule="0 0 * * *",  # Daily at midnight
    catchup=False,
    tags=["dataset_name", "extraction"],
)
def dataset_pipeline():
    """
    Pipeline de extração, transformação e carga.
    
    Fluxo:
    1. Inicia rastreamento de execução
    2. Extrai dados da fonte
    3. Transforma para o modelo de storage
    4. Carrega no banco
    5. Finaliza com sucesso ou erro
    """
    
    def get_control_repo():
        return ControlRepository(handler=PostgresHandler(engine=get_engine()))
    
    @task
    def start_pipeline():
        """Inicializa rastreamento de carga."""
        repo = get_control_repo()
        dataset_name = "dataset_name"
        load_id = repo.create_initial_load(dataset_name)
        return {"load_id": load_id, "dataset_name": dataset_name}
    
    @task
    def extract_data():
        """Responsabilidade Única: Extração."""
        extractor = <Dataset>Extractor(
            api_key=os.getenv("DATASET_API_KEY")
        )
        
        # Definir parâmetros de extração
        params = {
            "limit": 1000,
            "offset": 0
        }
        
        # Extrai e serializa para XCom
        raw_stream = extractor.fetch_stream(params)
        return [raw.model_dump(mode="json") for raw in raw_stream]
    
    @task
    def load_data(raw_data: list):
        """Responsabilidade Única: Transformação e Persistência."""
        if not raw_data:
            return 0
        
        handler = PostgresHandler(engine=get_engine())
        mapper = <Dataset>Mapper()
        repo = <Dataset>Repository(handler=handler)
        
        # Reconstrói DTOs do XCom
        raw_dtos = (<Dataset>RawDTO(**d) for d in raw_data)
        
        # Transforma e persiste
        storage_entities = list(mapper.transform_stream(raw_dtos))
        rows_affected = repo.upsert_batch(storage_entities)
        
        return rows_affected
    
    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def finalize_success(load_context: dict, rows_count: int):
        """Finaliza com sucesso."""
        repo = get_control_repo()
        load_dto = ETLLoadDTO(
            id=load_context['load_id'],
            dataset_name=load_context['dataset_name'],
            status=LoadStatus.SUCCESS,
            rows_extracted=rows_count,
            rows_loaded=rows_count,
            end_time=datetime.now()
        )
        repo.update_load_status(load_dto)
    
    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def handle_failure(load_context: dict, **context):
        """Finaliza com falha."""
        repo = get_control_repo()
        ti = context['ti']
        error_msg = f"Falha na task: {ti.task_id}"
        
        load_dto = ETLLoadDTO(
            id=load_context['load_id'],
            dataset_name=load_context['dataset_name'],
            status=LoadStatus.FAILED,
            error_message=error_msg,
            end_time=datetime.now()
        )
        repo.update_load_status(load_dto)
        raise Exception(error_msg)
    
    # Orquestração de fluxo
    load_ctx = start_pipeline()
    raw_list = extract_data()
    rows_affected = load_data(raw_list)
    
    finalize_success(load_ctx, rows_affected) >> load_ctx
    handle_failure(load_ctx, upstream_failed=True) >> load_ctx

# Instancia a DAG
pipeline = dataset_pipeline()
```

**Boas Práticas DAG:**
- Usar decoradores `@dag` e `@task`
- Uma função por responsabilidade
- Parametrizar valores (API keys, limites, etc.)
- Implementar ambas as rotas: sucesso e falha
- Usar `TriggerRule` para controlar fluxos

---

## Checklist de Implementação

### Models
- [ ] RawDTO definido com type hints completos
- [ ] StorageDTO definido com type hints e ConfigDict
- [ ] Ambos documentados com docstrings
- [ ] Validações Pydantic (se necessário)

### Services
- [ ] Extrator implementado com stream (generator)
- [ ] Mapper implementado com stream
- [ ] Retry/backoff implementado no Extrator
- [ ] Tratamento de erros apropriado

### Infrastructure
- [ ] Repository criado para o dataset
- [ ] Queries SQL em arquivos separados
- [ ] Métodos de persistência (upsert, insert)
- [ ] Handler de banco abstrato

### DAG
- [ ] Tasks com responsabilidades únicas
- [ ] Tratamento de sucesso e falha
- [ ] Rastreamento em Control Dataset
- [ ] Serialização/desserialização de XCom
- [ ] Documentação de tags e schedule

### Tests (recomendado)
- [ ] Testes unitários de Extrator
- [ ] Testes unitários de Mapper
- [ ] Testes de integração com banco (se possível)
- [ ] Testes de DAG com fixtures

---

## Referência de Dependências

Dependências típicas por camada:

```
DAG
├── require: Decorators, TriggerRule
├── require: ControlRepository, ControlDTO
└── require: Extrator, Mapper, Repository

Service (Extrator)
├── require: RawDTO
├── require: Generators, retry
└── optional: external client (pytrends, requests, etc.)

Service (Mapper)
├── require: RawDTO, StorageDTO
└── optional: enrichment services

Repository
├── require: StorageDTO, PostgresHandler
└── require: SQL queries

Models
└── require: Pydantic
```

---

## Troubleshooting Comum

### Problema: XCom muito grande
**Solução**: Usar batch pequenos ou armazenar em S3/temp storage

```python
# Ao invés de
return all_data  # Pode ser muito grande

# Usar
for batch in chunks(all_data, 100):
    ti.xcom_push(key=f"batch_{i}", value=batch)
```

### Problema: Rate limit em extração
**Solução**: Implementar backoff exponencial no Extrator

```python
def _safe_call(self, func, max_retries=5):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait = (2 ** i) * 5
            time.sleep(wait)
```

### Problema: Dados incorretos carregados
**Solução**: Validar em duas camadas:
1. Pydantic validation em DTOs
2. Lógica de validação em Mapper

```python
class <Dataset>RawDTO(BaseModel):
    value: int = Field(gt=0)  # Pydantic validation
```

---

## Recursos Adicionais

- [Airflow Task Decorators](https://airflow.apache.org/docs/apache-airflow/stable/howto/work-with-decorators.html)
- [Pydantic Models](https://docs.pydantic.dev/latest/)
- [Domain-Driven Design](https://en.wikipedia.org/wiki/Domain-driven_design)
- [Layered Architecture](https://en.wikipedia.org/wiki/Layered_architecture)

---

**Versão**: 1.0  
**Data**: 2026-08-30  
**Revisor**: Marca Platform Architecture
