# Documentação Arquitetural

Este diretório contém a documentação arquitetural do sistema, organizada para evoluir de forma incremental, versionável e com baixo acoplamento à tecnologia.

A documentação segue os princípios do **C4 Model** e **Architecture Decision Records (ADR)**, com diagramas mantidos como código.

## Ordem de Leitura Recomendada

A documentação segue uma progressão de conhecimento:

1. **Arquitetura** — O QUE o sistema é e como está estruturado
2. **Decisões** — POR QUE as escolhas arquiteturais foram feitas
3. **Deployment** — COMO o sistema está implementado atualmente
4. **Diagramas** — Representações visuais dos fluxos e componentes

## Arquitetura (Modelo C4)

Descrições conceituais e estáveis do sistema, independentes de tecnologia específica.

- `architecture/context.md` — Contexto do sistema, atores principais e integrações externas
- `architecture/containers.md` — Principais blocos de sistema e responsabilidades
- `architecture/components.md` — Decomposição estrutural dos componentes

## Decisões Arquiteturais (ADR)

Registro formal das decisões arquiteturais relevantes, alternativas consideradas e consequências.

Cada ADR documenta uma decisão importante e pode ser revisitada conforme o sistema evolui.

- `decisions/adr-001-separate-booking-and-payments-apis.md` — Separação de domínios de reservas e pagamentos
- `decisions/adr-002-bff-pattern.md` — Adoção de Backend-for-Frontend como orquestrador
- `decisions/adr-003-event-bus-pattern.md` — Comunicação assíncrona entre serviços
- `decisions/adr-004-analytics-db.md` — Estratégia de banco analítico separado

## Deployment (Estado Atual)

Documentação de como a arquitetura está implementada na prática. Estes documentos refletem o estado real e podem mudar com frequência.

- `deployment/current.md` — Topologia de deployment e componentes implementados

## Diagramas

Representações visuais dos fluxos, estrutura de containers e casos de uso.

- `diagrams/context.md` — Diagrama de contexto do sistema
- `diagrams/containers.md` — Diagrama de containers e dependências
- `diagrams/flow-booking-payments.md` — Fluxo de reserva e pagamento
- `diagrams/flow-analytics.md` — Fluxo de processamento de dados analíticos
- `diagrams/use-cases.md` — Casos de uso principais

## Convenções de Documentação

- Arquitetura conceitual não referencia tecnologia específica
- Tecnologias e trade-offs são documentados em ADRs
- Diagramas são representações visuais e complementam, não substituem, a documentação
- Alterações estruturais exigem atualização correspondente em `architecture/`
- Mudanças de tecnologia exigem nova ADR ou atualização da ADR existente
- Mudanças de implementação exigem atualização de `deployment/`

## Rastreabilidade

Toda decisão arquitetural deve ser localizável através de:

```text
requirement/use-case
   ↓
architecture
   ↓
decision (ADR)
   ↓
diagram (referência visual)
```
