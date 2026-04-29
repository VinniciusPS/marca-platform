```text
booking-service/
├── app/
│   ├── domain/
│   │   ├── entities.py
│   │   ├── value_objects.py
│   │   ├── events.py
│   │   ├── exceptions.py
│   │   └── repositories.py
│   │
│   ├── application/
│   │   ├── commands.py
│   │   ├── handlers.py
│   │   ├── consumers.py
│   │   └── message_bus.py
│   │
│   ├── infrastructure/
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── models.py
│   │   │   ├── repositories.py
│   │   │   └── uow.py
│   │   ├── messaging/
│   │   │   ├── outbox.py
│   │   │   └── publisher.py
│   │   └── schemas.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── dependencies.py
│   │
│   ├── main.py
│   └── worker.py
│
├── migrations/
└── tests/