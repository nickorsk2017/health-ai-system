# Monorepo Architecture Rules

## Structure
```
/
├── frontend/        # Next.js + Tailwind
├── backend/         # Python + FastAPI microservices
└── mcp-agents/      # Python + MCP AI agents
```

## Universal Rules

### Clean Code
- Functions do one thing. Names reveal intent.
- No comments. Self-documenting code only.
- Max 200 lines per file. Extract when exceeded.
- No dead code. No TODO comments. No debug logs committed.
- No abbreviations except industry-standard ones (id, url, api, db).

### Clean Architecture
- Dependencies point inward. Domain has no framework imports.
- Each layer owns its own types. No leaking across boundaries.
- No circular dependencies between modules.
- Side effects isolated to edges (I/O, DB, HTTP).

### Git
- One concern per commit. Conventional commits format.
- Feature branches off `main`. PRs required for merge.
- No secrets in code. Use environment variables.

### Cross-Service Contracts
- All inter-service communication via typed schemas.
- Breaking changes require versioning.
- MCP agents communicate with backend via HTTP only.
- Frontend communicates with backend via REST only.
