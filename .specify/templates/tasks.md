# Tasks — Pn

## 1. Objetivo

Implementar a especificação descrita em:

```text
spec.md
```

---

# 2. Dependências

```text
T001
 ↓
T002 ───→ T003
 ↓
T004
```

---

# 3. Fase 1 — Setup

* [ ] T001 Preparar estrutura inicial em `<path>`.
* [ ] T002 [P] Configurar dependência em `<path>`.

---

# 4. Fase 2 — Fundação

* [ ] T003 Implementar `<componente>` em `<path>`.
* [ ] T004 [P] Criar contrato em `<path>`.

---

# 5. Fase 3 — US1

## Objetivo

Implementar:

```text
US1
```

## Critério de conclusão

Todos os critérios `AC` associados devem ser satisfeitos.

### Implementação

* [ ] T005 [US1] Implementar `<comportamento>` em `<path>`.
* [ ] T006 [US1] Implementar validação em `<path>`.

### Testes

* [ ] T007 [US1] Criar testes unitários em `<path>`.
* [ ] T008 [US1] Criar teste de integração em `<path>`.

---

# 6. Fase 4 — US2

## Objetivo

Implementar:

```text
US2
```

### Implementação

* [ ] T009 [US2] ...

---

# 7. Fase final — Polish

* [ ] T010 Executar suíte de testes.
* [ ] T011 Executar benchmark.
* [ ] T012 Atualizar documentação.
* [ ] T013 Atualizar `checkpoint.md`.
* [ ] T014 Executar análise de consistência.

---

# 8. Dependências entre User Stories

```text
US1 → US2 → US3
```

---

# 9. Execução paralela

Exemplo:

```text
T005 ──┐
       ├──→ T009
T006 ──┘

T007 ─────→ T010
```

Tasks marcadas `[P]` podem ser executadas em paralelo quando suas dependências forem satisfeitas.

---

# 10. Estratégia

Implementar na seguinte ordem:

```text
Fundação
  ↓
MVP
  ↓
User Stories
  ↓
Integração
  ↓
Validação
  ↓
Benchmark
  ↓
Polish
```

---

# 11. Definition of Done

* [ ] Todas as tasks concluídas.
* [ ] Testes relevantes passando.
* [ ] Critérios de aceitação satisfeitos.
* [ ] Benchmark executado quando aplicável.
* [ ] Documentação atualizada.
* [ ] Checkpoint atualizado.
* [ ] Nenhum gap crítico conhecido.
