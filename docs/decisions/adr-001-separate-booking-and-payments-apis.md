# ADR-005: Separação de Agendamento e Pagamentos em APIs Distintas

## Status
Accepted

## Context

Agendamento e Pagamentos possuem:
- Regras de negócio distintas.
- Escalas diferentes.
- Ritmos de mudança diferentes.
- Responsabilidades conceituais separadas.

Manter ambos em uma única API aumentaria:
- Complexidade.
- Acoplamento.
- Risco de regressão.

## Decision

Os domínios de **Agendamento** e **Pagamentos** serão implementados como
**APIs separadas**, cada uma com:
- Banco de dados próprio.
- Ciclo de deploy independente.
- Contratos bem definidos.

## Alternatives Considered

### Alternative 1: API única (monólito lógico)

**Prós**
- Menor overhead inicial.
- Simplicidade de deploy.

**Contras**
- Acoplamento forte.
- Escalabilidade limitada.
- Dificuldade de evolução independente.

### Alternative 2: Separação por módulos internos

**Prós**
- Organização interna melhor.
- Menos infraestrutura.

**Contras**
- Deploy ainda acoplado.
- Boundaries frágeis.

### Alternative 3: APIs separadas (Chosen)

**Prós**
- Boundaries claros.
- Escala independente.
- Menor risco de impacto cruzado.
- Alinhamento com DDD.

**Contras**
- Mais serviços para operar.
- Comunicação distribuída.

## Consequences

### Positive
- Clareza de domínio.
- Independência de times e releases.
- Melhor observabilidade por domínio.

### Negative / Trade-offs
- Complexidade operacional maior.
- Necessidade de contratos e versionamento.

## Evidence / Metrics

### Success Criteria
- Deploy independente sem impacto cruzado.
- Escalabilidade distinta entre domínios.
- Falhas isoladas por serviço.

### Supporting Data
- Análise de carga mostrou padrões distintos:
  pagamentos com picos curtos e agendamento mais estável.
- Separação reduz blast radius de falhas.

## Related Decisions
- ADR-003: Event Bus
- ADR-002: BFF Pattern
