# ADR-002: Adoção do padrão Backend for Frontend (BFF)

## Status
Accepted

## Date
---

## Context

O frontend necessita realizar consultas e composições de dados que
envolvem múltiplos serviços de domínio (por exemplo, reservas e pagamentos).

Requisitos observados:

- UI precisa de respostas unificadas que combinam dados de mais de um
serviço.
- O frontend não deve ser obrigado a orquestrar diversas chamadas.
- Experiência do usuário (latência percebida) é um fator de qualidade.

Problemas em abordagens alternativas:

- **Frontend chamando diretamente múltiplos serviços**:
  - Lógica de composição espalhada na UI.
  - Duplica conhecimento de API em múltiplos clientes.
  - Dificulta versionamento e evolução das APIs.
- **Gateway API simples (sem agregação)**:
  - Reduz latência de chamadas, mas não reduz a complexidade das chamadas
    de composição do frontend.

## Decision

Será adotado um componente Backend for Frontend (BFF) como um
ponto de orquestração e agregação de dados entre o frontend e os serviços
do sistema.

O BFF serve como:

1. **Agregador de dados** — combina respostas de múltiplos serviços.
2. **Ponto de adaptação de API** — transforma modelos de serviços em
   modelos que fazem sentido para o frontend.
3. **Mediador de versão** — desacopla releases de backend de releases de
   frontend.

## Alternatives Considered

### Alternative 1: Frontend faz composição
- **Descrição**: O frontend realiza múltiplas requisições diretas aos serviços
  e faz a composição da informação.
- **Prós**:
  - Simplicidade inicial.
  - Menos código de backend a manter.
- **Contras**:
  - Lógica de orquestração espalhada entre páginas/aplicações.
  - Aumenta o acoplamento entre frontend e APIs.
  - Exposição de detalhes internos de serviços ao cliente.
  - Difícil evoluir ou versionar sem impacto no cliente.

### Alternative 2: API Gateway (sem agregação)
- **Descrição**: Um gateway que faz roteamento e segurança, mas não
  composição de respostas.
- **Prós**:
  - Permite centralizar autenticação/autorização.
  - Reduz número de endpoints conhecidos pelo cliente.
- **Contras**:
  - Não resolve a necessidade de composição de dados.
  - Frontend ainda precisa orquestrar múltiplas chamadas.

### Alternative 3: GraphQL Gateway
- **Descrição**: Um GraphQL que faz composição de esquemas de múltiplos
  serviços.
- **Prós**:
  - Poderosa abstração de dados.
  - Alta flexibilidade de consulta.
- **Contras**:
  - Curva de aprendizado maior.
  - Complexidade adicional de infraestrutura.
  - Não atende necessidade de forma mais simples do que BFF neste estágio.

## Consequences

### Positive
- **Frontend simplificado** — menos lógica de composição e menos surface area para testes UI.
- **Evolução desacoplada** — impacto menor quando serviços backend mudam.
- **Control point** para performance, caching e políticas cross-cutting (ex.: throttling).
- **Versões diversas** — BFF pode expor diferentes APIs para diferentes clientes (mobile, web).

### Negative / Trade-offs
- **Mais um componente para manter** — exige deploy, monitoramento e testes.
- **Potencial chokepoint** — se mal projetado, pode se tornar gargalo de performance.
- **Duplicação potencial de lógica de roteamento** — se não houver cuidado com composição padrão.

## Risks and Mitigation

| Risk | Mitigation |
|------|------------|
| BFF se torna monolítico com lógica complexa | Estabelecer limites claros, testes automatizados e princípios de simplicidade |
| Performance degradada no BFF | Adotar caching, métricas e monitorar latência por endpoint |
| Acoplamento forte entre BFF e serviços | Definir contratos de API claros e versionados |

## Evidence / Metrics

### Success Criteria (para validação)

1. **Tempo de resposta agregado menor que 2s** para requests compostas
   (ex.: reserva + pagamentos) sob carga de uso típico.
2. **Redução de chamadas do frontend de N → 1** para composições
   comuns de UI.
3. **Cobertura de testes automatizados ≥ 80%** nas rotas de orquestração.

### Supporting Data

- Simulações iniciais de carga mostraram que chamadas diretas
  simultâneas do frontend geram latências percebidas acima de 1.2s
  em cenários normais.  
- Com o BFF agregando dados e cache simples, a latência de respostas
  compostas caiu para ~750ms (ver `experiments/load-test-baseline.md`).
- Logs preliminares mostraram que páginas compostas exigiam em média
  4 chamadas separadas quando sem BFF.

![Evidências](docs/evidences)

## Related Decisions

- ADR-001: Analytics Assíncrono  
- Deployment assumptions (pode influenciar o pattern de escalabilidade)