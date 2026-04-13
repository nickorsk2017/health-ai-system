.PHONY: install run build

install:
	uv sync

run:
	uv run gateway

build:
	docker build -t health-gateway .
