```Mermaid
flowchart LR
%% Actors
Operador([Operador])
Financeiro([Financeiro])
Analista([Analista])
Gateway([Gateway de Pagamento Externo])

%% Use Cases
UC1((Criar Reserva))
UC2((Consultar Reservas))
UC3((Atualizar Status da Reserva))

UC4((Iniciar Pagamento))
UC5((Consultar Pagamentos))

UC6((Visualizar Relatórios))
UC7((Consultar Métricas))

%% Relationships
Operador --> UC1
Operador --> UC2
Operador --> UC3

Financeiro --> UC4
Financeiro --> UC5

Analista --> UC6
Analista --> UC7

UC4 --> Gateway
