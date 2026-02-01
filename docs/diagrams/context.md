```Mermaid
flowchart LR
User[Usuário Operacional]
Manager[Gestor]

User --> System[Marca Platform]
Manager --> System

System --> PaymentProvider[Provedor de Pagamento Externo]
