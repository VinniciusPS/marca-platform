```Mermaid
sequenceDiagram
actor Analista
participant Frontend
participant BFF
participant AnalyticsAPI
participant AnalyticsDB

Analista ->> Frontend: Consultar métricas
Frontend ->> BFF: GET /analytics
BFF ->> AnalyticsAPI: Query agregada
AnalyticsAPI ->> AnalyticsDB: Consulta OLAP
AnalyticsAPI -->> BFF: Resultado
BFF -->> Frontend: Métricas consolidadas
