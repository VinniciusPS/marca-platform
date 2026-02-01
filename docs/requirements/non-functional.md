# Quality Attributes (Non-Functional Requirements)

## Overview

Este documento define os requisitos não funcionais
que guiam as decisões arquiteturais do sistema.

---

## QA-01 — Performance

### Leituras Operacionais
- Tempo de resposta: < 500ms (p95)
- Worst case aceitável: < 1s

### Escritas Operacionais
- Tempo de resposta: < 1s (p95)
- Chamadas externas não bloqueantes

### Analytics
- Queries complexas: < 2–5s
- Não afetam APIs operacionais

---

## QA-02 — Throughput

- Suporte a até 50 usuários simultâneos.
- Até 20 requisições/segundo agregadas no BFF.
- Baixo volume absoluto, mas consistente.

---

## QA-03 — Availability

- SLA alvo:
  - APIs core: 99.5%
  - Analytics: 99%
- Falhas em pagamentos externos não devem derrubar o sistema.

---

## QA-04 — Consistency

- Consistência forte dentro de cada serviço.
- Consistência eventual entre serviços.
- Eventos entregues ao menos uma vez.
- Consumidores devem ser idempotentes.

---

## QA-05 — Scalability

- Escala vertical suficiente para o volume atual.
- Escala horizontal possível, mas não obrigatória.
- Serviços escalam independentemente.

---

## QA-06 — Security

- Autenticação centralizada no BFF.
- Autorização baseada em perfil:
  - Operacional
  - Financeiro
  - Analytics
- Dados sensíveis não trafegam em eventos.

---

## QA-07 — Observability

- Logs estruturados.
- Correlation-id entre serviços.
- Métricas básicas:
  - Latência
  - Erros
  - Processamento de eventos

---

## QA-08 — Cost Efficiency

- Infra simples (VMs ou serverless).
- Uso de Redis como broker.
- Evitar componentes complexos (Kafka, workflow engines).
