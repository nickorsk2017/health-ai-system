.PHONY: dev inspector kill-inspector inspector-docker build-docker

dev:
	uv run master_orchestrator_agent

inspector:
	make kill-inspector
	npx @modelcontextprotocol/inspector uv run master_orchestrator_agent

kill-inspector:
	kill -9 $$(lsof -t -i :6274 -i :6277) 2>/dev/null || true

inspector-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env master_orchestrator_agent

build-docker:
	docker build -t master_orchestrator_agent .

kill-port:
	kill -9 $$(lsof -t -i :6350) 2>/dev/null || true
