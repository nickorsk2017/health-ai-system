FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY . .

RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache .

EXPOSE 8001

CMD ["user_microservice"]
