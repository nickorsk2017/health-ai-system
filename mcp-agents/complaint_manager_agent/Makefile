.PHONY: dev inspector kill-inspector build-docker

dev:
	kill -9 $$(lsof -t -i :6341) 2>/dev/null || true
	uv run complaint-manager-agent

inspector:
	kill -9 $$(lsof -t -i :6274 -i :6277) 2>/dev/null || true
	npx @modelcontextprotocol/inspector uv run complaint-manager-agent

kill-inspector:
	kill -9 $$(lsof -t -i :6274 -i :6277) 2>/dev/null || true

build-docker:
	docker build -t complaint-manager-agent .
