# medical-consilium-agent

An MCP orchestrator that fetches a patient's full SOAP history from `visit_doctor_agent` and routes it through **9 specialist LLMs running in parallel**, returning only those specialists who identified clinically relevant findings.

## Tool

### `run_medical_consilium`

| Argument                    | Type   | Description                                      |
|-----------------------------|--------|--------------------------------------------------|
| `user_id`                   | string | Patient identifier                               |
| `start_date_clinic_history` | string | ISO 8601 start date for history search (`YYYY-MM-DD`) |

Returns a `list[SpecialistFinding]` — only from specialties that found relevant issues.

```json
[
  {
    "specialty": "cardiology",
    "risks": "...",
    "treatment": "...",
    "prognosis": "...",
    "probable_diagnosis": "..."
  }
]
```

## Architecture

```
run_medical_consilium(user_id, start_date)
        │
        ▼
HistoryClient.fetch()
  └─ MCP Client → visit_doctor_agent (get_doctor_visits_history)
        │
        ▼
ConsiliumService.run(records)
  └─ asyncio.gather(
       analyze(oncology),
       analyze(gastroenterology),
       analyze(cardiology),
       analyze(hematology),
       analyze(nephrology),
       analyze(nutrition),
       analyze(endocrinology),
       analyze(mental_health),
       analyze(pulmonology),
     )
        │
        ▼
Filter out is_relevant=false → return findings
```

## Setup

### Prerequisites

- `visit_doctor_agent` running in HTTP mode (see its README for `--transport http`)
- OpenAI API key

### 1. Environment variables

```bash
cp example.env .env
# Edit .env
```

| Variable                   | Description                                          |
|----------------------------|------------------------------------------------------|
| `OPENAI_API_KEY`           | OpenAI API key                                       |
| `OPENAI_MODEL`             | Model name (default: `gpt-4o-mini`)                 |
| `VISIT_DOCTOR_AGENT_URL`   | HTTP URL of the running visit_doctor_agent MCP server |

### 2. Start visit_doctor_agent in HTTP mode

```bash
cd ../visit_doctor_agent
uv run visit-doctor-mcp-agent --transport streamable-http --port 8080
```

### 3. Local development

```bash
make install
make inspect   # opens MCP Inspector at http://localhost:6274
```

## Docker

```bash
make build
make inspect-docker
```

Or run directly:
```bash
docker run -i --rm --env-file .env medical-consilium-agent
```
