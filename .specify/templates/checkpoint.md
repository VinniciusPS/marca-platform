# Checkpoint — Pn

## 1. Estado

```text
IN PROGRESS
```

Valores possíveis:

```text
NOT STARTED
IN PROGRESS
BLOCKED
READY FOR REVIEW
COMPLETED
```

---

# 2. Último estado conhecido

Data:

```text
YYYY-MM-DD HH:mm
```

Agente:

```text
<agent>
```

Última task:

```text
T###
```

---

# 3. Progresso

```text
Spec:      ✅
Plan:      ✅
Tasks:     🔄
Implement: 🔄
Tests:     ⏳
Benchmark: ⏳
```

---

# 4. Tasks concluídas

* [x] T001 ...
* [x] T002 ...

---

# 5. Próxima task

```text
T003
```

Descrição:

...

---

# 6. Decisões tomadas

## DEC-001

...

---

# 7. Problemas encontrados

## ISSUE-001

Problema:

...

Impacto:

...

Status:

```text
OPEN
```

---

# 8. Validações realizadas

| Validação        | Resultado | Evidência |
| ---------------- | --------- | --------- |
| Testes unitários | PASS      | ...       |
| Integração       | PASS      | ...       |
| Benchmark        | PENDING   | ...       |

---

# 9. Estado técnico

Arquivos modificados:

```text
<path>
```

Componentes afetados:

```text
<componente>
```

---

# 10. Próximos passos

1. ...
2. ...
3. ...

---

# 11. Contexto necessário para retomada

Um novo agente deve ler:

```text
AGENTS.md
Master-plan.md
docs/Pn/spec.md
docs/Pn/plan.md
docs/Pn/tasks.md
docs/Pn/checkpoint.md
```

e então continuar a partir de:

```text
T###
```

---

# 12. Handoff

### Instrução para o próximo agente

> Continue a implementação a partir de `T###`.
> Não recomece tasks concluídas.
> Verifique primeiro o estado descrito neste checkpoint.
> Em caso de conflito entre checkpoint e artifacts, siga a hierarquia definida em `AGENTS.md`.
