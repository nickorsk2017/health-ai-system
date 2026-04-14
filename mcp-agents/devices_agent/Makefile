.PHONY: dev inspector kill-inspector inspector-docker build-docker

dev:
	make kill-port
	uv run device-orchestrator-agent

inspector:
	make kill-inspector
	npx @modelcontextprotocol/inspector uv run device-orchestrator-agent

kill-inspector:
	kill -9 $$(lsof -t -i :6274 -i :6277) 2>/dev/null || true

inspector-docker:
	make kill-inspector
	npx @modelcontextprotocol/inspector docker run -i --rm --env-file .env device-orchestrator-agent

build-docker:
	docker build -t device-orchestrator-agent .

kill-port:
	kill -9 $$(lsof -t -i :6340) 2>/dev/null || true
