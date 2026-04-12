# Backend Rules

## Stack
- Python 3.12+, FastAPI, SQLAlchemy (async), Pydantic v2, Uvicorn

## Folder Map
```
backend/
├── _common/              # Shared across all microservices
│   ├── db/               # Base models, session factory
│   ├── schemas/          # Shared Pydantic schemas
│   └── env/              # Environment variable definitions
└── {name}-microservice/  # One folder per bounded context
    ├── routers/          # FastAPI route handlers
    ├── services/         # Business logic
    ├── models/           # SQLAlchemy ORM models
    ├── schemas/          # Pydantic request/response schemas
    └── main.py           # FastAPI app factory + Uvicorn entry
```

## Rules

### General
- No business logic in routers. Routers call service functions only.
- Services are pure Python functions. No FastAPI, no SQLAlchemy in services.
- Models define DB schema. Schemas define API contract. They are separate.
- All environment access through `_common/env/`. Never `os.environ` inline.
- No global state. Dependency injection via FastAPI `Depends`.

### Naming
- Routers: `{resource}_router.py` (e.g. `user_router.py`).
- Services: `{resource}_service.py` (e.g. `user_service.py`).
- Models: `{Resource}Model` class, `{resource}_model.py` file.
- Schemas: `{Resource}Schema`, `{Resource}CreateSchema`, `{Resource}ResponseSchema`.

### Error Handling
- Raise `HTTPException` only in routers.
- Services raise domain-specific Python exceptions.
- No bare `except:`. Always specify exception type.

### Database
- Async SQLAlchemy sessions only.
- Migrations via Alembic. No `create_all()` in production code.
- Transactions managed at service layer, not router.
