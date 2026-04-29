```Mermaid
sequenceDiagram
actor Operador
participant Frontend
participant BFF
participant ReservasAPI
participant ReservasDB
participant EventBus
participant PagamentosAPI
participant PagamentosDB
participant Gateway

Operador ->> Frontend: Criar reserva
Frontend ->> BFF: POST /reservas
BFF ->> ReservasAPI: Criar reserva (PENDING_PAYMENT)
ReservasAPI ->> ReservasDB: Persistir reserva
ReservasAPI -->> EventBus: ReservaCriada

EventBus -->> PagamentosAPI: ReservaCriada
PagamentosAPI ->> Gateway: Processar pagamento
Gateway -->> PagamentosAPI: Resultado
PagamentosAPI ->> PagamentosDB: Persistir pagamento

alt Pagamento confirmado
    PagamentosAPI -->> EventBus: PagamentoConfirmado
    EventBus -->> ReservasAPI: PagamentoConfirmado
    ReservasAPI ->> ReservasDB: Atualizar reserva → CONFIRMED
else Pagamento recusado
    PagamentosAPI -->> EventBus: PagamentoRecusado
    EventBus -->> ReservasAPI: PagamentoRecusado
    ReservasAPI ->> ReservasDB: Atualizar reserva → CANCELLED
end
