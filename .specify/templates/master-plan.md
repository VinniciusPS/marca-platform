# Master Plan

> Documento global de planejamento do projeto.
>
> Este documento responde **o que precisa ser resolvido, por que importa e em qual ordem**, sem duplicar a especificação ou o plano técnico de cada problema.

---

# 1. Visão do projeto

## 1.1 Objetivo

<!-- Descreva o estado futuro desejado em poucas linhas. -->

## 1.2 Resultado esperado

<!-- O que deverá ser verdade quando o projeto atingir seu objetivo? -->

## 1.3 Escopo global

### Incluído

* <!-- ... -->

### Fora de escopo

* <!-- ... -->

---

# 2. Princípios de planejamento

Este plano deve seguir:

1. Resolver primeiro problemas de maior valor esperado.
2. Priorizar redução de risco e desbloqueio de dependências.
3. Evitar dividir artificialmente uma mudança em múltiplos `Pn`.
4. Cada `Pn` deve representar uma unidade de mudança verificável.
5. Detalhes de requisitos pertencem ao `spec.md`.
6. Detalhes de arquitetura pertencem ao `plan.md`.
7. Trabalho executável pertence ao `tasks.md`.
8. Evidências de execução pertencem ao `checkpoint.md` e aos benchmarks.
9. Mudanças devem ser rastreáveis desde o problema até sua validação.

---

# 3. Mapa de problemas

Cada `Pn` representa um problema ou oportunidade que precisa ser resolvido.

| ID | Problema     | Objetivo     |         RICE | Status  | Dependências |
| -- | ------------ | ------------ | -----------: | ------- | ------------ |
| P1 | <!-- ... --> | <!-- ... --> | <!-- ... --> | BACKLOG | —            |
| P2 | <!-- ... --> | <!-- ... --> | <!-- ... --> | BACKLOG | P1           |
| P3 | <!-- ... --> | <!-- ... --> | <!-- ... --> | BACKLOG | —            |

### Status permitidos

```text
BACKLOG
READY
IN PROGRESS
BLOCKED
READY FOR REVIEW
COMPLETED
CANCELLED
```

---

# 4. Priorização RICE

## 4.1 Fórmula

```text
RICE = (Reach × Impact × Confidence) / Effort
```

## 4.2 Reach

Estime quantos usuários, execuções, entidades, processos ou unidades serão afetados durante o período considerado.

|  Valor | Interpretação  |
| -----: | -------------- |
|      1 | alcance mínimo |
|     10 | alcance baixo  |
|    100 | alcance médio  |
| 1.000+ | alcance alto   |

A unidade de Reach deve ser definida no contexto do projeto.

---

## 4.3 Impact

| Valor | Interpretação |
| ----: | ------------- |
|  0,25 | mínimo        |
|   0,5 | baixo         |
|     1 | médio         |
|     2 | alto          |
|     3 | massivo       |

---

## 4.4 Confidence

Representa a confiança nas estimativas de Reach e Impact.

| Valor | Interpretação |
| ----: | ------------- |
|   0,5 | baixa         |
|   0,8 | média         |
|   1,0 | alta          |

---

## 4.5 Effort

Estimativa do esforço necessário para entregar o `Pn`.

Unidade:

```text
<!-- definir: pessoa-dia, horas, story points etc. -->
```

---

# 5. Backlog priorizado

A ordem deve ser derivada do RICE, ajustada quando houver dependências ou redução de risco justificável.

| Ordem | ID | Problema     | Reach | Impact | Confidence | Effort | RICE | Dependências |
| ----: | -- | ------------ | ----: | -----: | ---------: | -----: | ---: | ------------ |
|     1 | P1 | <!-- ... --> |       |        |            |        |      |              |
|     2 | P2 | <!-- ... --> |       |        |            |        |      |              |
|     3 | P3 | <!-- ... --> |       |        |            |        |      |              |

### Regra

Um `Pn` com RICE inferior pode preceder outro quando existir:

* dependência técnica;
* bloqueio de outro `Pn`;
* risco crítico;
* requisito externo;
* necessidade de aprendizado;
* oportunidade de reduzir incerteza significativamente.

Toda exceção deve ser justificada em `Decisões de priorização`.

---

# 6. Registro de cada problema

## P1 — <nome do problema>

### Problema

<!-- Descrição curta do problema. -->

### Por quê?

<!-- Por que este problema importa? -->

### Resultado esperado

<!-- Qual resultado deve ser obtido? -->

### Hipótese

<!-- Qual hipótese está sendo validada? -->

### Métricas de sucesso

* <!-- ... -->

### Dependências

* <!-- Nenhuma / Pn -->

### RICE

```text
Reach:
Impact:
Confidence:
Effort:

RICE:
```

### Artefatos

```text
docs/P1/
├── spec.md
├── plan.md
├── tasks.md
├── checkpoint.md
└── benchmark.md
```

### Status

```text
BACKLOG
```

---

## P2 — <nome do problema>

### Problema

<!-- ... -->

### Por quê?

<!-- ... -->

### Resultado esperado

<!-- ... -->

### Hipótese

<!-- ... -->

### Métricas de sucesso

* <!-- ... -->

### Dependências

* <!-- ... -->

### RICE

```text
Reach:
Impact:
Confidence:
Effort:

RICE:
```

### Status

```text
BACKLOG
```

---

# 7. Dependências entre problemas

Representar somente dependências relevantes.

```text
P1 ──────→ P2
 │
 └──────→ P3

P4 ──────→ P5
```

### Matriz de dependências

| Problema | Depende de | Motivo       |
| -------- | ---------- | ------------ |
| P1       | —          | —            |
| P2       | P1         | <!-- ... --> |
| P3       | P1         | <!-- ... --> |

---

# 8. Roadmap

## Fase 1 — Fundação

<!-- Problemas que estabelecem infraestrutura, contratos ou conhecimento necessários. -->

* P1

## Fase 2 — Implementação principal

* P2
* P3

## Fase 3 — Otimização

* P4

## Fase 4 — Convergência

* validação global;
* benchmarks;
* documentação;
* resolução de gaps.

---

# 9. Estado global

| Pn | Spec | Clarify | Plan | Checklist | Tasks | Implementação | Validação | Benchmark | Status  |
| -- | ---- | ------- | ---- | --------- | ----- | ------------- | --------- | --------- | ------- |
| P1 | ⏳    | ⏳       | ⏳    | ⏳         | ⏳     | ⏳             | ⏳         | ⏳         | BACKLOG |
| P2 | ⏳    | ⏳       | ⏳    | ⏳         | ⏳     | ⏳             | ⏳         | ⏳         | BACKLOG |

Legenda:

```text
⏳ Não iniciado
🔄 Em andamento
✅ Concluído
⚠️ Bloqueado
N/A Não aplicável
```

---

# 10. Decisões de priorização

Registrar somente decisões que alteram a ordem ou o escopo global.

## PRI-001 — <decisão>

### Contexto

<!-- ... -->

### Decisão

<!-- ... -->

### Motivo

<!-- ... -->

### Impacto

<!-- ... -->

---

# 11. Decisões globais

Decisões que afetam múltiplos `Pn`.

| ID      | Decisão      | Motivo       | Problemas afetados |
| ------- | ------------ | ------------ | ------------------ |
| ADR-001 | <!-- ... --> | <!-- ... --> | P1, P2             |

Decisões específicas de um único `Pn` devem permanecer em:

```text
docs/Pn/plan.md
```

---

# 12. Riscos globais

| ID       | Risco        | Probabilidade    | Impacto          | Mitigação    | Pn |
| -------- | ------------ | ---------------- | ---------------- | ------------ | -- |
| RISK-001 | <!-- ... --> | Baixa/Média/Alta | Baixo/Médio/Alto | <!-- ... --> | P1 |

---

# 13. Hipóteses globais

| ID    | Hipótese     | Evidência atual | Como validar | Status |
| ----- | ------------ | --------------- | ------------ | ------ |
| H-001 | <!-- ... --> | <!-- ... -->    | P1           | OPEN   |

Status:

```text
OPEN
VALIDATED
INVALIDATED
DEFERRED
```

---

# 14. Métricas globais

| Métrica      | Baseline | Meta | Atual | Fonte |
| ------------ | -------: | ---: | ----: | ----- |
| <!-- ... --> |          |      |       |       |

---

# 15. Benchmark global

Benchmarks específicos devem permanecer em:

```text
docs/Pn/benchmark.md
benchmarks/Pn-benchmark.py
```

Este documento deve conter apenas resultados agregados relevantes para a visão global.

| Métrica      | Baseline | Atual | Meta | Resultado |
| ------------ | -------: | ----: | ---: | --------- |
| <!-- ... --> |          |       |      |           |

---

# 16. Registro de aprendizado

Registrar somente aprendizados que alterem decisões futuras.

## LEARN-001

### Observação

<!-- ... -->

### Evidência

<!-- ... -->

### Impacto

<!-- ... -->

### Ação

<!-- ... -->

---

# 17. Gaps conhecidos

| ID      | Gap          | Impacto      | Pn relacionado | Ação         |
| ------- | ------------ | ------------ | -------------- | ------------ |
| GAP-001 | <!-- ... --> | <!-- ... --> | P1             | <!-- ... --> |

Nenhum gap deve ser ocultado para fazer o projeto parecer concluído.

---

# 18. Critério de conclusão global

O projeto poderá ser considerado concluído quando:

* [ ] Todos os objetivos globais relevantes forem satisfeitos.
* [ ] Todos os `Pn` críticos forem concluídos.
* [ ] Critérios de sucesso forem validados.
* [ ] Benchmarks relevantes forem executados.
* [ ] Riscos críticos estiverem tratados ou explicitamente aceitos.
* [ ] Gaps críticos estiverem resolvidos ou formalmente aceitos.
* [ ] Documentação estiver consistente.
* [ ] Não existirem contradições conhecidas entre especificação, plano, tasks e implementação.

---

# 19. Convenção de artefatos

Cada `Pn` deve seguir:

```text
docs/Pn/
├── spec.md
├── plan.md
├── tasks.md
├── checkpoint.md
├── benchmark.md
├── checklist.md
└── research.md
```

Nem todos os artefatos são obrigatórios para mudanças triviais.

### Obrigatórios para mudanças relevantes

```text
spec.md
plan.md
tasks.md
checkpoint.md
```

### Condicionais

```text
benchmark.md
checklist.md
research.md
```

---

# 20. Rastreabilidade global

O projeto deve permitir navegar:

```text
Master Plan
    │
    ▼
Problem Pn
    │
    ▼
Requirement FR/US
    │
    ▼
Acceptance Criteria
    │
    ▼
Plan / Decision
    │
    ▼
Task Txxx
    │
    ▼
Código
    │
    ▼
Teste
    │
    ▼
Benchmark
    │
    ▼
Evidência
```

Cada `Pn` deve possuir documentação suficiente para reconstruir essa cadeia.

---

# 21. Próxima ação

> <!-- O próximo agente deve conseguir identificar a próxima ação relevante sem reler todo o projeto. -->

**Próximo Pn:**

```text
Pn
```

**Próxima etapa:**

```text
<!-- specify / clarify / plan / tasks / implement / validate / converge -->
```

**Próxima ação:**

```text
<!-- ação concreta -->
```

**Fonte:**

```text
<!-- documento/task que autoriza a ação -->
```