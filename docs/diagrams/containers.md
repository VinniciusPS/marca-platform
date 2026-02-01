```Mermaid
flowchart LR
Frontend[Web] --> BFF[BFF]

BFF --> Reservas[Reservas API]
BFF --> Pagamentos[Pagamentos API]
BFF --> Analytics[Analytics API]

Reservas --> ReservasDB[(Reservas DB)]
Pagamentos --> PagamentosDB[(Pagamentos DB)]

Reservas --> EventBus[[Event Bus]]
Pagamentos --> EventBus

ReservasDB --- AnalyticsJobs[Analytics Jobs]
PagamentosDB --- AnalyticsJobs[Analytics Jobs]
AnalyticsJobs --> AnalyticsDB[(Analytics DB)]

Pagamentos --> External[Gateway de Pagamento Externo]
