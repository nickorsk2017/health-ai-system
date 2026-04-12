# visit-doctor-mcp-agent

An MCP agent that records and retrieves specialist medical consultations in **SOAP format**, backed by PostgreSQL.

## Tools

### `add_visit_doctor`

Records a new consultation.

| Argument      | Type   | Required | Description |
|---------------|--------|----------|-------------|
| `doctor_type` | string | yes      | Specialty: `oncology`, `gastroenterology`, `cardiology`, `hematology`, `nephrology`, `nutrition`, `endocrinology`, `mental_health`, `pulmonology` |
| `subjective`  | string | yes      | Patient complaints and history |
| `objective`   | string | yes      | Clinical findings and vitals |
| `assessment`  | string | yes      | Diagnosis or clinical impression |
| `date_visit`  | string | yes      | ISO 8601 date (`YYYY-MM-DD`) |
| `user_id`     | string | yes      | Patient identifier |
| `plan`        | string | no       | Treatment plan or next steps |

Returns: `{"success": true, "visit_id": "<uuid>"}`

---

### `get_doctor_visits_history`

Retrieves SOAP notes from a start date to today.

| Argument          | Type   | Required | Description |
|-------------------|--------|----------|-------------|
| `last_date_visit` | string | yes      | ISO 8601 start date (`YYYY-MM-DD`) |
| `user_id`         | string | yes      | Patient identifier |
| `doctor_type`     | string | no       | Filter by specialty |

Returns: list of full SOAP note objects.

---

## Database schema

```sql
CREATE TABLE visits (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      VARCHAR(255) NOT NULL,
    doctor_type  VARCHAR(50)  NOT NULL,
    date_visit   DATE         NOT NULL,
    subjective   TEXT         NOT NULL,
    objective    TEXT         NOT NULL,
    assessment   TEXT         NOT NULL,
    plan         TEXT,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX ON visits (user_id);
CREATE INDEX ON visits (doctor_type);
CREATE INDEX ON visits (date_visit);
```

Tables are created automatically on agent startup via SQLAlchemy `create_all`.

## Setup

### 1. Environment variables

```bash
cp example.env .env
# Edit .env — set DATABASE_URL to your PostgreSQL instance
```

`DATABASE_URL` format:
```
postgresql+asyncpg://user:password@host:5432/database_name
```

### 2. Local development

Requires [uv](https://github.com/astral-sh/uv) and a running PostgreSQL instance.

```bash
make install   # create .venv and install dependencies
make inspect   # open MCP Inspector at http://localhost:6274
```

## Docker

### Build

```bash
make build
```

### Run (stdio transport)

```bash
docker run -i --rm --env-file .env visit-doctor-mcp-agent
```

### MCP Inspector (Docker)

```bash
make inspect-docker
```
