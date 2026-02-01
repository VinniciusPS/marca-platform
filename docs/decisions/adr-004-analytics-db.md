# ADR-004: Adoção de Banco OLAP para Analytics

## Status
Accepted

## Context

O sistema possui necessidades de:
- Análises históricas.
- Consultas agregadas complexas.
- Relatórios com grandes volumes de dados.
- Baixo impacto no tráfego transacional.

O banco transacional (OLTP) é otimizado para escrita e leitura pontual,
não para consultas analíticas intensivas.

## Decision

Será adotado um **banco OLAP dedicado** para workloads analíticos,
alimentado de forma assíncrona a partir de eventos e dados operacionais.

O banco OLAP não participa de fluxos transacionais.

## Alternatives Considered

### Alternative 1: Consultas analíticas no banco OLTP

**Prós**
- Menor custo inicial.
- Menos infraestrutura.

**Contras**
- Impacto direto em performance transacional.
- Locks e contenção.
- Escalabilidade limitada.

### Alternative 2: Replicas de leitura do OLTP

**Prós**
- Isola parcialmente carga.
- Fácil implementação.

**Contras**
- Não resolve consultas analíticas complexas.
- Ainda dependente do modelo transacional.

### Alternative 3: OLAP dedicado (Chosen)

**Prós**
- Isolamento total de carga analítica.
- Modelagem orientada a leitura.
- Escalabilidade horizontal.
- Queries rápidas em grandes volumes.

**Contras**
- Pipeline de dados adicional.
- Consistência eventual.

## Consequences

### Positive
- Nenhum impacto no desempenho transacional.
- Relatórios e dashboards rápidos.
- Base sólida para BI e ML futuro.

### Negative / Trade-offs
- Dados não são em tempo real.
- Necessidade de governança de dados.
- Complexidade de ETL/ELT.

## Evidence / Metrics

### Success Criteria
- Zero queries analíticas no OLTP.
- Dashboards respondendo em < 2s.
- Latência de ingestão aceitável (< minutos).

### Supporting Data
- Testes mostraram degradação de até 30% no OLTP sob carga analítica.
- OLAP reduziu tempo médio de consulta de minutos para segundos.

## Related Decisions
- ADR-003: Event Bus
