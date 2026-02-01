# Functional Requirements

## Overview

Este documento descreve os requisitos funcionais
em nível arquitetural para um sistema interno de gestão
de reservas, pagamentos e analytics.

O sistema é utilizado por empresas de serviços
com até 100 usuários internos.

---

## FR-01 — Gestão de Reservas

O sistema deve permitir que usuários do módulo operacional:

- Criem reservas de serviços.
- Consultem reservas por múltiplos critérios.
- Atualizem status da reserva (criada, confirmada, cancelada).
- Visualizem histórico de alterações.

Volume esperado:
- Até 3 criações de reserva por minuto.
- Até 10 consultas por minuto em pico.

---

## FR-02 — Processamento de Pagamentos

O sistema deve permitir:

- Iniciar pagamentos vinculados a uma reserva.
- Integrar-se com um gateway externo de pagamentos.
- Registrar estados: pendente, aprovado, recusado.
- Garantir idempotência para requisições repetidas.

Características:
- Baixo volume, alta criticidade.
- Falhas externas não devem bloquear o sistema.

---

## FR-03 — Comunicação Assíncrona entre Domínios

O sistema deve:

- Publicar eventos de domínio relevantes:
  - ReservaCriada
  - PagamentoAprovado
  - PagamentoRecusado
- Permitir consumo assíncrono dos eventos.
- Suportar reprocessamento em caso de falha.

---

## FR-04 — Analytics Operacional

O sistema deve permitir:

- Visualização de métricas agregadas:
  - Reservas por período
  - Taxa de conversão de pagamentos
- Consultas históricas sem impacto no fluxo operacional.

Restrições:
- Dados não precisam ser em tempo real.
- Atraso aceitável de minutos.

---

## FR-05 — Backend for Frontend (BFF)

O sistema deve expor um BFF que:

- Centraliza autenticação.
- Orquestra chamadas a múltiplos serviços.
- Fornece modelos de leitura otimizados para o frontend.
