# Especificação — P1

## 1. Metadados

| Campo | Valor |
| --- | --- |
| ID | P1 |
| Nome | Estado atual da arquitetura |
| Status | CURRENT_STATE |
| Prioridade | P1 |
| Autor | Copilot |
| Data | 2026-08-30 |
| Master Plan | `../../Master-plan.md` |

---

## 2. Problema

O repositório apresenta múltiplas camadas arquiteturais e padrões de implementação em evolução, mas não existe uma documentação única e verificável do estado atual do conjunto de componentes, integrações e fluxos de dados. Há discrepância entre a arquitetura conceitual documentada e o nível de implementação concreta.

---

## 3. Contexto

O projeto foi documentado como uma plataforma para gestão de reservas, pagamentos e analytics, com foco em operação clínica/serviços. A documentação conceitual declara BFF, domínios separados e analytics em banco OLAP, enquanto o código real possui implementações parciais e estruturas em diferentes níveis de maturidade.

Essa situação exige um documento de arquitetura atual baseado em evidência, explicitando:

- o que efetivamente existe no repositório;
- o que está planejado ou parcialmente implementado;
- quais integrações e fluxos foram observados;
- quais lacunas e incertezas persistem.

---

## 4. Motivação

A correção deste documento é necessária para evitar conclusões baseadas em suposições. A arquitetura deve ser registrada com evidência verificável antes de qualquer mudança de implementação ou design.

---

## 5. Objetivo

Registrar o estado real da arquitetura do repositório em português, com distinção entre:

- fatos observados;
- inferências sólidas;
- hipóteses;
- itens não confirmados.

---

## 6. Fora de escopo

* OUT-001 — Criação de backlog de implementação ou tarefas técnicas.
* OUT-002 — Alteração de código, infra, dependências, CI/CD ou comportamento em runtime.
* OUT-003 — Definição de arquitetura futura sem evidência no código/documentação existente.

---

## 7. Usuários / atores

| ID | Ator | Necessidade |
| -- | --- | --- |
| A1 | Operador/usuário funcional | Consumir reserva e processos operacionais. |
| A2 | Financeiro | Acompanhar pagamentos e estados financeiros. |
| A3 | Gestor/analista | Consultar métricas e indicadores de performance. |
| A4 | Sistema externo de pagamento | Receber e responder transações financeiras. |
| A5 | ETL/analytics | Extrair, transformar e entregar dados analíticos. |

---

## 8. User Stories

## US1 — Documentar o estado atual da arquitetura

**Como** mantenedor do repositório
**Quero** entender a arquitetura real do sistema
**Para** reduzir risco em mudanças futuras e manter a documentação alinhada com o código.

### Critérios de aceitação

#### AC1

**Dado que** o repositório contém múltiplas camadas e tecnologias

**Quando** o documento for revisado

**Então** ele deve listar os componentes observados, suas localizações e estado de implementação.

#### AC2

**Dado que** o repositório possui documentação conceitual e implementações parciais

**Quando** a arquitetura for documentada

**Então** o texto deve separar fatos observados, inferências e incertezas sem inventar elementos ausentes.

---

## 9. Requisitos funcionais

## FR-001

O documento deve descrever os principais componentes arquiteturais presentes no repositório.

## FR-002

O documento deve mapear as tecnologias, módulos e responsabilidades observadas em cada camada.

## FR-003

O documento deve descrever os fluxos de dados e integrações externos identificados no código e na documentação.

## FR-004

O documento deve registrar a persistência e a modelagem de dados observados nas migrações e schemas.

## FR-005

O documento deve distinguir claramente:

- fatos observados;
- inferências; 
- hipóteses;
- itens desconhecidos.

---

## 10. Requisitos não funcionais

## NFR-001 — Clareza de documentação

A arquitetura documentada deve ser legível e verificável por outros agentes sem depender da memória da sessão.

## NFR-002 — Evidência

Cada asserção deve estar apoiada em arquivos do repositório, documentação ou código observado.

## NFR-003 — Segurança

A documentação não deve expor segredos, URLs internas ou credenciais em ambientes reais. Placeholder deve ser usado quando necessário.

---

## 11. Restrições

* O documento não pode alterar comportamento funcional em qualquer componente.
* O documento não pode criar tarefas de implementação.
* O documento deve seguir a hierarquia de autoridade do `AGENTS.md`.
* O documento deve refletir o repositório em seu estado atual, não a visão de um futuro desejado.

---

## 12. Casos-limite

| Caso | Comportamento esperado |
| ---- | ---------------------- |
| Repositório com arquitetura incompleta | A documentação deve indicar o status parcial e os pontos não implementados. |
| Divergência entre documentação e código | A documentação deve registrar a diferença explicitamente. |
| Falta de evidência para uma decisão | O texto deve sinalizar como hipótese ou desconhecido. |
| Existe infraestrutura REST/ETL sem runtime completo | O documento deve descrever a estrutura observada sem afirmar produção final. |

---

## 13. Critérios de sucesso

## SC-001

O arquivo de documentação identifica corretamente os principais componentes e suas localizações no sistema.

## SC-002

O texto separa fatos observados de inferências e hipóteses sem inventar elementos ausentes.

## SC-003

A documentação descreve o funcionamento básico dos fluxos de dados e persistência observados.

---

## 14. Métricas

| Métrica | Baseline | Meta |
| ------- | -------: | ---: |
| Cobertura de componentes principais | 0 | ≥ 100% dos diretórios principais rastreados |
| Separação entre fato/inferência | 0 | 100% dos pontos relevantes discriminados |
| Evidência documentada | 0 | 100% das afirmações com origem em repositório |

---

## 15. Questões em aberto

* [ ] Q1 — Qual é o ambiente de produção real e a infraestrutura definitiva para reservas/pagamentos?
* [ ] Q2 — Há broker/Event Bus operacional em produção ou a documentação ainda representa um desenho futuro?
* [ ] Q3 — O BFF e as APIs de reservas/pagamentos são entregues em outras branches ou ainda estão em desenvolvimento parcial?

---

## 16. Glossário

| Termo | Definição |
| ----- | --------- |
| Brownfield | Repositório que mistura desenho arquitetural, infraestrutura parcialmente implementada e código em diferentes estágios de maturidade. |
| BFF | Backend for Frontend: camada de composição e adaptação entre frontend e serviços. |
| OLAP | Banco analítico orientado a leitura e agregações históricas. |
| ETL | Extração, transformação e carregamento de dados. |

---

## 17. Rastreabilidade

| Requirement | User Story | Critério | Métrica |
| ----------- | ---------- | -------- | ------- |
| FR-001 | US1 | AC1 | SC-001 |
| FR-003 | US1 | AC2 | SC-003 |
| FR-005 | US1 | AC2 | SC-002 |
