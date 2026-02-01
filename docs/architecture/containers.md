# Containers do Sistema

## Visão Geral
Este documento descreve os principais blocos do sistema e suas responsabilidades.

## Containers

### Frontend
- Interface de interação com usuários
- Responsável pela experiência do usuário

### Backend for Frontend (BFF)
- Orquestra chamadas entre frontend e serviços
- Agrega dados para operações de leitura

### Serviço de Reservas
- Gerencia o ciclo de vida de reservas
- Emite eventos de domínio relacionados a reservas

### Serviço de Pagamentos
- Processa pagamentos
- Integra-se com provedores externos
- Emite eventos de pagamento

### Serviço de Analytics
- Consolida dados operacionais
- Fornece métricas e relatórios
