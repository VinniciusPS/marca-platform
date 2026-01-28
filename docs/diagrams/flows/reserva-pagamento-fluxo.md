```mermaid
sequenceDiagram
    participant U as Usuario
    participant W as Web App
    participant B as BFF
    participant R as Reservas Service
    participant P as Pagamentos Service
    participant Red as Redis

    U->>W: Criar reserva
    W->>B: POST /reservas
    B->>R: createReserva
    R-->>B: Reserva criada

    R->>Red: Evento ReservaCriada

    U->>W: Registrar pagamento
    W->>B: POST /pagamentos
    B->>P: processarPagamento
    P-->>B: Pagamento confirmado

    P->>Red: Evento PagamentoConfirmado
    B-->>W: Sucesso
