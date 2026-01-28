
```mermaid
sequenceDiagram
    participant U as Usuario
    participant W as Web App
    participant B as BFF
    participant A as Analytics Service
    participant DB as Postgres Analytics

    U->>W: Abrir dashboard
    W->>B: GET /analytics
    B->>A: consultarMetricas
    A->>DB: query
    DB-->>A: dados agregados
    A-->>B: resposta
    B-->>W: dashboard renderizado
