FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY _common/ _common/
COPY backend/user_microservice/ .

RUN uv pip install --system --no-cache .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 8001

CMD ["user_microservice"]
