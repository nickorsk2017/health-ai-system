# MCP Agents Rules

## Stack
- Python 3.12+, FastMCP

## Purpose
AI agents that expose tools via MCP and communicate with the backend via HTTP only.

## Structure
```
mcp-agents/
├── _common/
│   ├── http_client.py    # Shared async HTTP client (httpx)
│   └── env/
│       └── settings.py   # Environment variables
└── {name}-agent/
    ├── schemas/
    │   ├── {model_name}.py # Domain models
    │   └── http.py       # HTTP request / response contracts
    ├── tools/
    │   └── {tool_name}.py # tools MCP
    ├── prompts/
    │   └── {prompt_name}.py
    ├── config.py         # Settings
    └── main.py           # MCP server entry point
```

## Rules

### General
- Each agent is an independent MCP server. One concern per agent.
- No shared state between tool calls. Tools are stateless functions.

### schemas/

- `*.py` — domain-level Pydantic models (e.g. `DailyBiometrics`). No framework imports.
- `http.py` — request and response models for backend HTTP contracts (e.g. `GetBiometricsRequest`, "").
- Never define Pydantic models inside `tools/` or `main.py`. All models live in `schemas/`.

### tools/
- One file per tool. Tool name matches filename.
- Tool functions are `async`. Accept typed parameters. Return typed results.
- Raise descriptive exceptions on failure — MCP surfaces these to the model.

### prompts/
- System prompt templates for the agent's persona and task framing.
- Plain Python strings or template functions. No logic.

### main.py Pattern
```python
from fastmcp import FastMCP

mcp = FastMCP("agent-name")

@mcp.tool()
def tool_name(param: str) -> str:
    """Tool description."""
    return result

@mcp.resource("config://settings")
def get_config() -> str:
    return "key: value"

if __name__ == "__main__":
    mcp.run()
```

- The `[project.scripts]` entry in `pyproject.toml` points to `main:run`.

## config.py Pattern

Every agent must have a `config.py` that loads env vars through `pydantic-settings`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str  # add fields for every required env var

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
```

- Import `settings` directly in tool files — never call `os.getenv` elsewhere in the agent.
- Each agent ships an `example.env` listing all fields with placeholder values and comments.
- Never commit `.env`. It is covered by `.gitignore`.

## Makefile

Every agent must ship a `Makefile` with the following standard targets:

```makefile
.PHONY: run-dev run-inspector kill-inspector run-inspector-docker build-docker

run-dev:
    uv run <agent-name>

run-inspector:
    make kill-inspector
    npx @modelcontextprotocol/inspector uv run <agent-name>

kill-inspector:
    kill -9 $$(lsof -t -i :6274 -i :6277) 2>/dev/null || true

run-inspector-docker:
    make kill-inspector
    npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env <agent-name>

build-docker:
    docker build -t <agent-name> .
```

| Target                | Purpose                                                    |
|-----------------------|------------------------------------------------------------|
| `run-dev`             | Run the agent locally via the `uv` script entry point      |
| `run-inspector`       | Open MCP Inspector UI against the local process            |
| `kill-inspector`      | Kill processes on ports 6274 (UI) and 6277 (proxy)         |
| `run-inspector-docker`| Open MCP Inspector UI against the built Docker image       |
| `build-docker`        | Build the Docker image                                     |

- `run-inspector` and `run-inspector-docker` always call `kill-inspector` first to free ports.
- `kill-inspector` prevents `make` from failing when no process holds the ports.
- `.env` is loaded automatically by `config.py` — no manual env passing needed for `run-dev`.