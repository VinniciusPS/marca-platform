# Arquitetura do Sistema

Este diretório contém a documentação arquitetural do sistema, organizada para
evoluir de forma incremental, versionável e com baixo acoplamento à tecnologia.

A documentação segue os princípios do **C4 Model**, **Architecture Decision Records (ADR)**
e **diagramas como código**.

---

## 🎯 Como ler esta documentação

A documentação é organizada por **níveis de estabilidade**.

Recomenda-se a seguinte ordem de leitura:

1. **Arquitetura (O QUE o sistema é)**
2. **Decisões (POR QUE ele é assim)**
3. **Deployment (COMO ele está implementado hoje)**
4. **Experimentos (EVIDÊNCIAS que suportam decisões)**

---

## 🧱 Arquitetura (C4)

Documentos conceituais e estáveis que descrevem o sistema independentemente de
tecnologia ou implementação.

- `architecture/context.md`  
  Contexto do sistema, atores e integrações externas.

- `architecture/containers.md`  
  Principais blocos do sistema e suas responsabilidades.

- `architecture/use-cases.md`  
  Casos de uso e cenários principais.

- `architecture/components/`  
  Nível de componentes (quando aplicável).

---

## 🧠 Decisões Arquiteturais (ADR)

Registro das decisões arquiteturais relevantes, incluindo alternativas consideradas
e consequências.

Cada ADR representa **uma decisão importante** e pode ser revisitada ao longo do tempo.

- `decisions/adr-001-analytics-async.md`  
- `decisions/adr-002-bff-pattern.md`

---

## 🚀 Deployment (estado atual)

Documentos que descrevem **como a arquitetura está implementada atualmente**.
Estes documentos são considerados voláteis e podem mudar com frequência.

- `deployment/current.md`  
- `deployment/assumptions.md`

---

## 🧪 Experimentos e Evidências

Resultados de experimentos, testes de carga e medições utilizados para validar
ou orientar decisões arquiteturais.

- `experiments/load-test-baseline.md`
- `experiments/analytics-offload.md`
- `experiments/redis-impact.md`

---

## 📐 Diagramas

Os diagramas arquiteturais são mantidos como código utilizando Mermaid.

- Código-fonte: `diagrams/`
- Imagens renderizadas: `images/`

As imagens são **geradas automaticamente** e não devem ser editadas manualmente.

---

## 🔄 Evolução da arquitetura

A arquitetura é esperada evoluir ao longo do tempo.

Boas práticas:
- Mudanças estruturais → atualizar **Arquitetura**
- Mudanças de tecnologia → criar ou atualizar **ADR**
- Mudanças de infra → atualizar **Deployment**
- Decisões relevantes → registrar evidências em **Experimentos**

---

## 📌 Convenções

- Arquitetura conceitual não referencia tecnologia específica
- Tecnologias e trade-offs são documentados apenas em ADRs
- Diagramas são representações visuais, não a fonte da verdade
- Este README é o único ponto de navegação entre documentos

---

## 🧭 Público-alvo

Esta documentação é destinada a:
- Desenvolvedores
- Tech Leads
- Arquitetos
- Stakeholders técnicos

O objetivo é facilitar entendimento, discussão e evolução do sistema.
