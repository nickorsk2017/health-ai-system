.PHONY: up down build logs ps restart clean nuke

up:
	docker compose up -d

build:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

restart:
	docker compose down && docker compose up -d

clean:
	docker compose down --volumes --remove-orphans

nuke:
	docker compose down --volumes --remove-orphans --rmi all
