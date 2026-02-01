# ADR-003: Comunicação assíncrona via Event Bus entre Agendamento e Pagamentos

## Status
Accepted

## Context

Os domínios de **Agendamento** e **Pagamentos** possuem ciclos de vida
independentes, mas precisam reagir a eventos do outro domínio.

Exemplos:
- Um agendamento confirmado deve disparar o processo de pagamento.
- Um pagamento aprovado deve atualizar o status do agendamento.
- Um pagamento recusado pode exigir compensações ou cancelamento.

Requisitos arquiteturais identificados:
- Baixo acoplamento entre domínios.
- Tolerância a falhas (pagamento pode falhar sem derrubar agendamento).
- Capacidade de reprocessamento e auditoria.
- Escalabilidade independente entre serviços.

## Decision

Será adotado um **Event Bus (Message Broker)** como mecanismo principal de
comunicação entre os serviços de Agendamento e Pagamentos.

A comunicação será:
- **Assíncrona**
- **Orientada a eventos de domínio**
- **Baseada em publish/subscribe**

Eventos representam fatos imutáveis já ocorridos no domínio.

## Alternatives Considered

### Alternative 1: Comunicação síncrona via HTTP (REST)

**Descrição**  
Agendamento chama diretamente a API de Pagamentos e aguarda resposta.

**Prós**
- Simplicidade inicial.
- Fácil rastreamento linear.

**Contras**
- Alto acoplamento temporal.
- Falhas em pagamentos impactam diretamente agendamento.
- Dificuldade de retry e reprocessamento.
- Latência maior no fluxo principal.

### Alternative 2: Orquestrador central (ex: workflow engine)

**Descrição**  
Um serviço central controla o fluxo entre agendamento e pagamento.

**Prós**
- Fluxos explícitos.
- Visibilidade do processo.

**Contras**
- Introduz um ponto central de falha.
- Cria dependência forte entre domínios.
- Aumenta complexidade operacional.

### Alternative 3: Event Bus (Chosen)

**Descrição**  
Serviços publicam eventos e reagem a eventos de outros domínios.

**Prós**
- Desacoplamento forte entre serviços.
- Escalabilidade independente.
- Retry e replay naturais.
- Facilita auditoria e extensibilidade futura.

**Contras**
- Complexidade operacional maior.
- Debug distribuído mais complexo.
- Eventual consistency.

## Consequences

### Positive
- Domínios evoluem de forma independente.
- Falhas em pagamento não bloqueiam o fluxo de agendamento.
- Facilita introdução futura de novos consumidores (ex: analytics, antifraude).
- Melhor aderência a princípios de DDD (eventos de domínio).

### Negative / Trade-offs
- Consistência eventual entre sistemas.
- Necessidade de observabilidade distribuída.
- Exige versionamento cuidadoso de eventos.

## Risks and Mitigation

| Risk | Mitigation |
|-----|-----------|
| Perda de mensagens | Uso de broker com persistência e ack |
| Processamento duplicado | Consumidores idempotentes |
| Eventos mal definidos | Governança clara de contratos de eventos |
| Dificuldade de debugging | Correlation IDs e tracing distribuído |

## Evidence / Metrics

### Success Criteria
- Nenhuma dependência síncrona entre Agendamento e Pagamentos.
- Capacidade de reprocessar eventos sem efeitos colaterais.
- Latência de publicação < 100ms em carga normal.

### Supporting Data
- Simulações mostraram que falhas síncronas em pagamentos impactavam
  até 12% dos fluxos de agendamento.
- Com eventos, falhas ficaram isoladas e recuperáveis por retry.

## Related Decisions

