.PHONY: install run build

install:
	uv sync

run:
	uv run user_microservice

build:
	docker build -t health-user-microservice .
