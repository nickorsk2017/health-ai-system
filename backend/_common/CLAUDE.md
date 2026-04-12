# _common Rules

## Purpose
Shared infrastructure used by all microservices. No business logic here.

## Structure
```
_common/
├── db/
│   ├── base.py       # DeclarativeBase, async session factory
│   └── mixins.py     # Shared column mixins (id, timestamps)
├── schemas/
│   └── base.py       # Shared Pydantic base config
└── env/
    └── settings.py   # All environment variables via pydantic-settings
```

## Rules

### db/
- `base.py` exports `Base` (SQLAlchemy DeclarativeBase) and `get_session` (async generator).
- `mixins.py` defines reusable column sets. Applied via multiple inheritance.
- No microservice-specific models here.

### schemas/
- Shared Pydantic config only (e.g. `model_config = ConfigDict(from_attributes=True)`).
- No domain-specific fields.

### env/
- Single `Settings` class via `pydantic-settings`.
- All env vars declared here with types and defaults.
- Microservices import from here. Never read `os.environ` directly.

## Pattern: Settings
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

## Forbidden
- Importing from any microservice folder
- Business logic
- FastAPI route definitions
